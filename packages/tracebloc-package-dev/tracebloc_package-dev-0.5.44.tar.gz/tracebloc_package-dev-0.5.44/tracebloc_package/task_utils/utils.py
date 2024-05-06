import tensorflow as tf
import numpy as np
import torchvision.datasets as datasets
from importlib.machinery import SourceFileLoader
import base64
import os
import ast
import pickle
import pickletools
from ..task_utils.constants import *
from ..task_utils.object_detection_utils import *
from ..task_utils.keypoint_detection_utils import FakeKeypointDetectionDataset

def check_MyModel(filename, path):
    try:
        # check if file contains the MyModel function
        model = SourceFileLoader(filename, f"{path}").load_module()
        model.MyModel(input_shape=(500, 500, 3), classes=10)
        return True, model

    except AttributeError:
        return (
            False,
            "Model file not provided as per docs: No function with name MyModel",
        )
    except TypeError:
        return (
            False,
            "Model file not provided as per docs: MyModel function receives no arguments",
        )
    except ValueError:
        return False, "Layers shape is not compatible with model input shape"


def is_model_supported(model_obj):
    tensorflow_supported_apis = (tf.keras.models.Sequential, tf.keras.Model)
    supported = isinstance(model_obj, tensorflow_supported_apis)
    if supported:
        # check if it of subclassing
        try:
            # Note that the `input_shape` property is only available for Functional and Sequential models.
            input_shape = model_obj.input_shape
            return True
        except AttributeError:
            return False


# function to check if layers used in tensorflow are supported
def layer_instance_check(model):
    model_layers = model.layers
    for layer in model_layers:
        if not isinstance(layer, tf.keras.layers.Layer):
            return False, []
    return True, model_layers


def is_valid_method(text):
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        return False
    return True


def get_base64_encoded_code(code):
    if not is_valid_method(code):
        raise ValueError("Input is not a valid Python method")
    code_bytes = code.encode("utf-8")
    return base64.b64encode(code_bytes).decode("utf-8")


def getImagesCount(images_count):
    count = 0
    for key in images_count.keys():
        count += images_count[key]
    return count


def get_model_info(model):
    # For Sequential model
    if isinstance(model, tf.keras.Sequential):
        # Get the input shape
        try:
            model_input_shape = model.input_shape[1:]
        except:
            raise ValueError(
                "Unable to determine input shape for the Sequential model."
            )

        # Get the number of output classes
        try:
            model_output_classes = model.layers[-1].units
        except:
            raise ValueError(
                "Unable to determine number of output classes for the Sequential model."
            )

    # For Functional model
    elif isinstance(model, tf.keras.Model):
        # Get the input shape
        try:
            model_input_shape = model.layers[0].input_shape[0][1:]
        except:
            raise ValueError(
                "Unable to determine input shape for the Functional model."
            )

        # Get the number of output classes
        try:
            output_shape = model.output_shape
            if len(output_shape) == 2:
                model_output_classes = output_shape[1]
            else:
                raise ValueError
        except:
            raise ValueError(
                "Unable to determine number of output classes for the Functional model."
            )

    else:
        raise ValueError("Model is neither Sequential nor Functional.")

    return model_input_shape, model_output_classes


def dummy_dataset_tensorflow(
    input_shape, num_classes, batch_size=8, num_examples=1000, category=IMAGE_CLASSIFICATION
):
    if category == IMAGE_CLASSIFICATION:
        # Create random images
        images = np.random.randint(0, 256, size=(num_examples,) + input_shape).astype(
            np.uint8
        )
        # Create random labels
        labels = np.random.randint(0, num_classes, size=(num_examples,))
        # One-hot encode the labels
        labels = tf.keras.utils.to_categorical(labels, num_classes=num_classes)

        # Convert to TensorFlow datasets
        ds = tf.data.Dataset.from_tensor_slices((images, labels))

        return ds.batch(batch_size)
    else:
        return None


def dummy_dataset_pytorch(
    image_size,
    num_classes=2,
    num_images=50,
    num_channels=3,
    category=IMAGE_CLASSIFICATION,
    model_type="",
):
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    )

    if category == IMAGE_CLASSIFICATION:
        image_shape = (num_channels, image_size, image_size)
        train_dataset = datasets.FakeData(
            size=num_images,
            image_size=image_shape,
            num_classes=num_classes,
            transform=transform,
        )
        return train_dataset

    elif category == OBJECT_DETECTION:
        image_shape = (448, 448)

        fake_dataset = FakeObjectDetectionDataset(
            num_classes=num_classes, num_samples=10, transform=transform
        )
        classes = fake_dataset.get_classes()
        if model_type == YOLO:
            train_dataset = create_yolo_dataset(
                dataset=fake_dataset, classes=classes, image_shape=image_shape, S=7, B=2
            )
            return train_dataset

        else:
            train_dataset = create_fasterrcnn_dataset(
                dataset=fake_dataset, classes=classes, image_shape=image_shape
            )
            return train_dataset
    elif category == KEYPOINT_DETECTION:
        if type(image_size) is int:
            image_shape = (image_size, image_size)
        else:
            image_shape = image_size

        fake_dataset = FakeKeypointDetectionDataset(
            image_size=image_shape,
            num_images=num_images,
            num_classes=num_classes,
            transform=transform
        )
        return fake_dataset


def get_model_parameters(**kwargs) -> None:
    model = kwargs["model"]
    framework = kwargs["framework"]

    if framework == PYTORCH_FRAMEWORK:
        if not kwargs["preweights"]:
            parameters = [val.cpu().numpy() for _, val in model.state_dict().items()]
        else:
            model.load_state_dict(torch.load(PRETRAINED_WEIGHTS_FILENAME, map_location=torch.device('cpu')))
            parameters = [val.cpu().numpy() for _, val in model.state_dict().items()]
    else:
        parameters = model.get_weights()

    weight_file_path = kwargs["weight_file_path"]
    weights_file_name = kwargs["weights_file_name"]

    with open(os.path.join(weight_file_path, f"{weights_file_name}.pkl"), "wb") as f:
        pickled = pickle.dumps(parameters)
        optimized_pickle = pickletools.optimize(pickled)
        f.write(optimized_pickle)

    del parameters


def get_model_output(model) -> int:
    dummy_data = np.random.rand(1, 224, 224, 3)
    # Get prediction
    predictions = model.predict(dummy_data)

    # return the class output
    return np.argmax(predictions[0])


def validate_kwargs(
    kwargs, allowed_kwargs, error_message="Keyword argument not understood:"
):
    """Checks that all keyword arguments are in the set of allowed keys."""
    for kwarg in kwargs:
        if kwarg not in allowed_kwargs:
            raise TypeError(error_message, kwarg)


def get_model_params_count(framework="tensorflow", model=None) -> int:
    """
    calculate total trainable parameters of a given model
    """
    if framework == TENSORFLOW_FRAMEWORK:
        return model.count_params()
    else:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
