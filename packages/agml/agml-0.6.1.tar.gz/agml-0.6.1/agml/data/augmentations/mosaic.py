# Copyright 2021 UC Davis Plant AI and Biophysics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import albumentations as A

import torch
from torch.utils.data import Dataset

import agml


class MosaicDataset(object):
    """Wraps an `AgMLDataLoader` using the mosaic transform.

    In essence, this class batches an `AgMLDataLoader` by the number of
    images to include in a mosaic, resulting in each call to get a piece
    of data returning a single mosaic.

    The `AgMLDataLoader` should already be constructed with all the
    desired parameters, such as transforms or image size conversion. Also,
    in order to work with `EfficientDet` training, it should be specifically
    transformed with a `TransformApplier` class.
    """
    def __init__(self,
                 loader: agml.data.AgMLDataLoader,
                 images_per_mosaic: int = 4):
        # There should always be full mosaics, no partial ones. This drops a potential
        # extra batch which might not have enough images for a mosaic,
        self._loader = loader.take_random((len(loader) // images_per_mosaic) * images_per_mosaic)
        if images_per_mosaic not in [4, 9, 16, 25]:
            raise ValueError("Invalid value for `images_per_mosaic`.")
        self._images_per_mosaic = images_per_mosaic
        self._loader.batch(batch_size = images_per_mosaic)

    def __len__(self):
        return len(self._loader)

    def __getitem__(self, indx):
        # Get the batch of images and annotations.
        images, annotations, *_ = self._loader[indx]

        # Get constant parameters.
        height, width = images[0].shape[1:]
        images_per_dim = int(np.sqrt(self._images_per_mosaic))

        # Create the output image mosaic, and adapt annotations as well.
        mosaic = np.zeros(shape = (3, height * images_per_dim, width * images_per_dim))
        mosaic_annotations = {'bboxes': [], 'labels': [], 'img_size': [], 'img_scale': []}

        # Get the mosaic row and column for the current image.
        row_col = lambda num: (num // images_per_dim, num % images_per_dim)

        # Build the mosaic.
        tracker = 0
        for image, annotation in zip(images, annotations):
            # Get the row and column for the image.
            row, col = row_col(tracker)

            # Update the image within the mosaic.
            mosaic[:, col * height: (col + 1) * height, row * width: (row + 1) * width] = image

            # Update the bounding boxes by the offset.
            new_annotation = annotation.copy()
            bboxes = new_annotation['bboxes']
            bboxes[:, 0] += col * height
            bboxes[:, 1] += row * width
            bboxes[:, 2] += col * height
            bboxes[:, 3] += row * width
            mosaic_annotations['bboxes'].append(bboxes)
            mosaic_annotations['labels'].append(new_annotation['labels'])

            # Increment the tracker.
            tracker += 1

        # Construct the sample.
        sample = {
            "image": np.array(mosaic, dtype = np.float32),
            "bboxes": mosaic_annotations['bboxes'],
            "labels": mosaic_annotations['labels']}

        # Augment the sample.
        sample = A.Compose(
            [A.Resize(height = 1024, width = 1024, p = 1)], p = 1.0,
            bbox_params = A.BboxParams(
                format = "pascal_voc", min_area = 0,
                min_visibility = 0, label_fields = ["labels"]))(**sample)

        # Return the sample.
        mosaic, mosaic_annotations = sample['image'], \
                                     {'bboxes': sample['bboxes'],
                                      'labels': sample['labels']}

        # Post-process the annotations.
        mosaic_annotations['bboxes'] = torch.concat(mosaic_annotations['bboxes'], dim = 0)
        mosaic_annotations['labels'] = torch.concat(mosaic_annotations['labels'], dim = 0)
        mosaic_annotations['img_size'] = torch.tensor(mosaic.shape[1:])
        mosaic_annotations['img_scale'] = torch.tensor([1.0])

        # Return the image and annotations.
        return mosaic, mosaic_annotations


