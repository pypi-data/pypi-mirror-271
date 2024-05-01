from typing import Literal, Optional
import uuid
import random
import hashlib

def create_id(id_type: Literal["uuid", "random", "hashed"], prefix: Optional[str] = "", size: Optional[int] = None) -> str:
    """
    Generate a unique identifier based on the specified type. The ID can be a UUID, a random number, or a hashed value.

    Examples:
        ```python
        import id_generator
        id_generator.create_id(id_type="uuid", prefix="item_", size=36)
        id_generator.create_id(id_type="random", size=16)
        id_generator.create_id(id_type="hashed", prefix="user", size=64)
        ```

    Args:
        id_type (str): Type of ID to generate. Options: 'uuid', 'random', 'hashed'.
        prefix (str): Optional prefix to prepend to the ID. Defaults to an empty string.
        size (Optional[int]): Length to truncate the ID. Defaults to the full length of the generated ID.

    Returns:
        str: The generated ID, possibly truncated to the specified size.

    Raises:
        ValueError: If `id_type` is not recognized.
    """
    if id_type == "uuid":
        # Generate a UUID
        result_id = str(uuid.uuid4())
    elif id_type == "random":
        # Generate a random number
        result_id = str(random.randint(1, 10**20))  # Adjust range or method as necessary
    elif id_type == "hashed":
        # Create a hash of UUID combined with random number
        unique_id = str(uuid.uuid4())
        random_number = random.randint(1, 1000000)
        hasher = hashlib.sha256()
        hasher.update(f"{prefix}{unique_id}{random_number}".encode())
        result_id = hasher.hexdigest()
    else:
        raise ValueError("Invalid 'id_type'. Options: 'uuid', 'random', 'hashed'.")

    # Truncate the ID if a size is specified
    if size is not None:
        result_id = result_id[:size]

    return f"{prefix}{result_id}"

# Example usage
if __name__ == "__main__":
    print(create_id(id_type="uuid", prefix="item_", size=36))
    print(create_id(id_type="random", size=16))
    print(create_id(id_type="hashed", prefix="user_", size=64))
