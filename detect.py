from ultralytics import YOLO
import cv2


def apply_mosaic(image, x1, y1, x2, y2, mosaic_size=5):
    """
    Apply a mosaic filter to the specified region in the image.

    Args:
    - image: Input image
    - x1, y1, x2, y2: Coordinates of the region to apply mosaic filter
    - mosaic_size: Size of the mosaic tiles

    Returns:
    - Image with applied mosaic filter
    """
    roi = image[y1:y2, x1:x2]
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_NEAREST)
    image[y1:y2, x1:x2] = cv2.resize(
        roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST
    )
    return image


def main(model_path, img_path, output_path):
    # Load a pretrained YOLOv8n model
    model = YOLO(model_path)

    # Run inference on an image
    image_path = img_path
    results = model(image_path)

    # Read the image
    image = cv2.imread(image_path)

    for r in results:
        print(
            r.boxes.xyxy
        )  # Print the Boxes object containing the detection bounding boxes
        for rect in r.boxes.data.tolist():
            # Extract target box coordinates (x, y, w, h)
            target_x, target_y, target_w, target_h = map(int, rect)

            # Apply mosaic filter to the target region
            image = apply_mosaic(image, target_x, target_y, target_w, target_h)

    # Save the image with applied mosaic filter
    cv2.imwrite(output_path, image)


if __name__ == "__main__":
    model_path = "best.pt"
    origin_path = "test.jpg"
    output_path = "output.jpg"
    main(model_path=model_path, img_path=origin_path, output_path=output_path)
