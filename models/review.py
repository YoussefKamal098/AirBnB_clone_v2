"""
This module defines the Review class, which inherits from the BaseModel class.

Classes:
    - Review

Attributes:
    - place_id (str): The ID of the place associated with the review.
    - user_id (str): The ID of the user who wrote the review.
    - text (str): The content of the review.

Methods:
    - No additional methods.

"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class represents a review of a place.

    Attributes:
        - place_id (str): The ID of the place associated with the review.
        - user_id (str): The ID of the user who wrote the review.
        - text (str): The content of the review.

    Methods:
        - No additional methods.
    """

    place_id: str = ""
    user_id: str = ""
    text: str = ""
