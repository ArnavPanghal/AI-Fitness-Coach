import math
from mediapipe.framework.formats import landmark_pb2

# Calculate angle between three points (shoulder, elbow, wrist)
def calculate_angle(a, b, c):
    a = [a.x, a.y, a.z]
    b = [b.x, b.y, b.z]
    c = [c.x, c.y, c.z]

    ab = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
    bc = [c[0] - b[0], c[1] - b[1], c[2] - b[2]]

    # Compute the cosine of the angle between the vectors
    ab_mag = math.sqrt(ab[0] ** 2 + ab[1] ** 2 + ab[2] ** 2)
    bc_mag = math.sqrt(bc[0] ** 2 + bc[1] ** 2 + bc[2] ** 2)
    dot_product = ab[0] * bc[0] + ab[1] * bc[1] + ab[2] * bc[2]
    cos_angle = dot_product / (ab_mag * bc_mag)

    # Return the angle in degrees
    angle = math.acos(cos_angle)
    return math.degrees(angle)
