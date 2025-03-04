def frames(ms: int, i_fps: float, o_fps: float) -> str:
    """
    Convert milliseconds to frame count based on output frame rate.
    
    Args:
        ms: Time in milliseconds
        i_fps: Input frames per second
        o_fps: Output frames per second
    
    Returns:
        String representation of the frame number
    """
    return str(int(ms / 1000 * o_fps))
