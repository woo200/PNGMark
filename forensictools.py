import struct
import bitman
import io

import numpy as np

F_MARK = b'\x9b\xbc3\x9a\xff\xe7h>\xafa+\x00\xe1\xa3\xa7\xdd'

class ForensicMark:
    def __init__(self, author: str, contact_email: str, license: str, copyright_notice: str):
        self._author = author
        self._contact_email = contact_email
        self._license = license
        self._copyright = copyright_notice

    def get_data(self):
        payload = b''

        payload += struct.pack("<B", len(self._author))
        payload += self._author.encode()

        payload += struct.pack("<B", len(self._contact_email))
        payload += self._contact_email.encode()

        payload += struct.pack("<B", len(self._license))
        payload += self._license.encode()

        payload += struct.pack("<B", len(self._copyright))
        payload += self._copyright.encode()

        return F_MARK + struct.pack("<H", len(payload)) + payload # payload length CANNOT be over 1024 bytes (will check later)

    def find_indexes(data, target):
        indexes = [-1]
        try:
            while True:
                indexes.append(data.index(target, indexes[-1] + 1))
        except (ValueError):
            pass
        return indexes[1:]

    def most_common(lst):
        return max(set(lst), key=lst.count)

    @staticmethod
    def get_mark(data):
        if F_MARK not in data:
            raise Exception("No forensic marks found")
        marks = []

        indexes = ForensicMark.find_indexes(data, F_MARK)
        for i in indexes:
            try:
                length, = struct.unpack("<H", data[i + 16:i + 18])
            except (struct.error):
                continue
            if length > 1024:
                continue
            if i + 18 + length > len(data):
                continue
            marks.append(data[i + 18:i + 18 + length])

        mark = ForensicMark.most_common(marks)
        mark = io.BytesIO(mark)

        author_len, = struct.unpack("<B", mark.read(1))
        author = mark.read(author_len).decode(errors="ignore")

        contact_email_len, = struct.unpack("<B", mark.read(1))
        contact_email = mark.read(contact_email_len).decode(errors="ignore")

        license_len, = struct.unpack("<B", mark.read(1))
        license = mark.read(license_len).decode(errors="ignore")

        notice_len, = struct.unpack("<B", mark.read(1))
        notice = mark.read(notice_len).decode(errors="ignore")

        return ForensicMark(author, contact_email, license, notice)

    def __repr__(self):
        return f"ForensicMark(copyright_holder={self._author}, contact_email={self._contact_email}, license={self._license}, notice={self._copyright})"

class BitPlanes:
    PLANE_LSB = 0

    def __closest(num, arr=[0, 255]):
        return min(arr, key=lambda x: abs(x - num))
    
    def get_bitplane(image: np.array, plane=PLANE_LSB):
        manipulator = bitman.BitManipulator()
        blank_image = np.zeros(image.size, dtype=np.uint8)

        for i, px in enumerate(image.flatten()):
            blank_image[i] = 255 if manipulator.check_bit(px, plane) else 0
        
        return blank_image.reshape(image.shape)
    
    def set_bitplane(image: np.array, new_plane: np.array, plane: int):
        manipulator = bitman.BitManipulator()

        normalized_bp = [BitPlanes.__closest(v) for v in new_plane.flatten()]
        new_image_flattened = image.flatten()

        for i, px in enumerate(new_image_flattened):
            new_image_flattened[i] = manipulator.set_bit(px, plane) if normalized_bp[i] == 255 else manipulator.clear_bit(px, plane)

        return new_image_flattened.reshape(image.shape)