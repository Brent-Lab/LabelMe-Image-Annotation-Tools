import os
import sys
import piexif
import piexif.helper


def set_exif_user_comment(img_dir, comment):
    """
    Replaces the UserComment section on an image's EXIF data with a new comment.

    Parameters:
        img_dir (string): Directory of the image being modified.
        comment (string): Comment which will be set in the UserComment section.

    Returns:
        None
    """
    exif_dict = piexif.load(img_dir)
    full_comment_dump = piexif.helper.UserComment.dump(comment)
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = full_comment_dump
    piexif.insert(piexif.dump(exif_dict), img_dir)


def set_exif_from_annotations(annotations, exif_label_map):
    """
    Takes a LabelMeAnnotation array and sets it's corresponding images' EXIF data using a dictionary mapping to the
    label and the comment.

    Parameters:
        annotations (list(LabelMeAnnotation)): List of LabelMeAnnotation classes.
        exif_label_map (dict(string, string)): Dictionary in the form of "LabelName : Comment".

    Returns:
        count (int): Number of images whose EXIF data has been set.
    """
    count = 0
    for annotation in annotations:
        img_dir = annotation.globalImagePath
        annotation_labels = annotation.get_labels()
        comment = ""
        
        for label in annotation_labels:
            if label in exif_label_map:
                comment = comment + exif_label_map[label] + ";"
        
        comment = comment[:-1] + ":"  # Replace last ; with a : indicating end of comment.
        set_exif_user_comment(img_dir, comment)
        count += 1

    return count
