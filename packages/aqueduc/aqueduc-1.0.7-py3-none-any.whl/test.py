import unittest
import aqueduc
import os

class TestAqueduc(unittest.TestCase):

    def create_test_file(self, path):
        f = open(path, "a")
        f.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
        f.close()

    def test_extension_forbidden_valid(self):
        self.assertEqual(aqueduc.extension_forbidden("test/folder/test.json", {"forbidden_extensions": []}), False, "Should be false")

    def test_extension_forbidden(self):
        self.assertEqual(aqueduc.extension_forbidden("test/folder/test.json", {"forbidden_extensions": ["json"]}), True, "Should be forbidden")

    def test_file_too_large(self):
        file_path = "test.txt"
        self.create_test_file(file_path)
        self.assertEqual(aqueduc.file_toolarge(file_path, {"size_limit": 500}), True, "Should be too large")
        os.remove(file_path)

    def test_file_not_too_large(self):
        file_path = "test.txt"
        self.create_test_file(file_path)
        self.assertEqual(aqueduc.file_toolarge(file_path, {"size_limit": 1000}), False, "Should not be too large")
        os.remove(file_path)

    def test_file_not_modified_since_date(self):
        file_path = "test.txt"
        self.create_test_file(file_path)
        self.assertEqual(aqueduc.file_not_modified_since_date(file_path, {"last_date_allowed": "27 04 2124 10"}), True, "Should not have been modified since date")
        os.remove(file_path)

    def test_file_modified_since_date(self):
        file_path = "test.txt"
        self.create_test_file(file_path)
        self.assertEqual(aqueduc.file_not_modified_since_date(file_path, {"last_date_allowed": "25 04 2024 10"}), False, "Should have been modified since date")
        os.remove(file_path)

    def test_remove_existing_file(self):
        file_path = "test.txt"
        self.create_test_file(file_path)
        self.assertEqual(aqueduc.try_remove_existing("", file_path), True, "Should have removed file")

    def test_remove_existing_folder(self):
        folder_name = "src"
        os.mkdir(folder_name,777)
        self.assertEqual(aqueduc.try_remove_existing(os.getcwd(), os.getcwd()), True, "Should have removed folder")


if __name__ == '__main__':
    unittest.main()
