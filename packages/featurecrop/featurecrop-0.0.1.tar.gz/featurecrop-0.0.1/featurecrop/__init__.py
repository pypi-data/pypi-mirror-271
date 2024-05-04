import numpy as np
import cv2


def featurecrop(image: np.ndarray, show_contours: bool = False) -> np.ndarray:
    """
    Smart auto-cropping.
    """

    def _autocrop(_image: np.ndarray) -> np.ndarray:
        """
        https://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil
        """
        image_data = np.asarray(_image)
        image_data_bw = image_data.max(axis=2)
        non_empty_columns = np.where(image_data_bw.max(axis=0) > 0)[0]
        non_empty_rows = np.where(image_data_bw.max(axis=1) > 0)[0]
        cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
        image_data_new = image_data[cropBox[0]:cropBox[1] + 1, cropBox[2]:cropBox[3] + 1, :]
        return image_data_new

    original_image = np.array(image)
    if show_contours:
        original_image_preview = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_uint8 = cv2.convertScaleAbs(laplacian)
    _, thresholded = cv2.threshold(laplacian_uint8, 30, 255, cv2.THRESH_BINARY)
    contours_outer, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(thresholded, contours_outer, -1, (255, 255, 255), 2)
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if show_contours:
        cv2.drawContours(image, contours_outer, -1, (255, 0, 0), 2)
        cv2.drawContours(image, contours, -1, (0, 255, 0), 1)

    def is_contour_closed(_contour: np.ndarray) -> bool:
        first_point = _contour[0][0]
        last_point = _contour[-1][0]
        return np.all(np.abs(np.subtract(last_point, first_point)) == 1)

    closed_contours = list()
    for idx, contour in enumerate(contours):
        if is_contour_closed(contour) and len(contour) > 1:
            closed_contours.append((idx, hierarchy[0][idx]))
    closures = list()
    for idx in closed_contours:
        closures.append(idx[0])
    counts = {id_: 0 for id_ in closures}
    for arr in hierarchy:
        arr = arr[arr != -1]
        unique, counts_per_arr = np.unique(arr, return_counts=True)
        for id_, count in zip(unique, counts_per_arr):
            if id_ in counts.keys():
                counts[id_] += count
    max_count_id = max(counts, key=lambda id_: counts[id_])

    target_contour = contours[max_count_id]
    total_area = image.shape[0] * image.shape[1]
    contour_area = cv2.contourArea(target_contour)
    percentage = (contour_area / total_area) * 100

    if percentage > 30:
        x, y, w, h = cv2.boundingRect(
            target_contour
        )
        x1, y1 = x + w, y + h
        original_image = _autocrop(original_image[y:y1, x:x1])

    if show_contours:
        cv2.rectangle(image, (x, y), (x1, y1), (0, 0, 255), 5)  # noqa
        cv2.imshow("original", original_image_preview)  # noqa
        cv2.imshow('Contours', image)
        cv2.imshow('Output', original_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return original_image
