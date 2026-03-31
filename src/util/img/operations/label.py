def label(self, label: str, rect: tuple[int, int, int, int], color=HOT_PINK, text_color=BLACK):
    """
    Draws a 1px border around the specified rectangle (x, y, w, h).
    The border is drawn 1px outside the bounds to avoid covering content.
    Includes a text label with a solid background.
    """
    x, y, w, h = rect
    
    # Draw the Bounding Box (1px outside)
    top_left = (x - 1, y - 1)
    bottom_right = (x + w, y + h)
    cv2.rectangle(self._data, top_left, bottom_right, color, 1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    thickness = 1
    padding = 4
    
    # Calculate text size (width, height), baseline
    (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)

    # Draw Text Background Rectangle, -1 thickness fills the rectangle
    bg_top_left = (x - 1, y - 1 - text_h - baseline - padding * 2)
    bg_bottom_right = (x - 1 + text_w + padding * 2, y - 1)
    cv2.rectangle(self._data, bg_top_left, bg_bottom_right, color, -1)

    # Draw the Text
    text_origin = (x - 1 + padding, y - 1 - baseline - padding)
    cv2.putText(self._data, label, text_origin, font, font_scale, text_color, thickness, cv2.LINE_AA)