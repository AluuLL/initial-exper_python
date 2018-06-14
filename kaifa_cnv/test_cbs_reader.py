import unittest
import cbs_reader
from mock import patch, mock_open


class MyTestCase(unittest.TestCase):
    def test_something(self):

        data = '\t'.join(['N1', 'chr1', '100', '200']) + '\n'
        print (data)
        with patch("builtins.open", mock_open(read_data=data)) as mock_file:
            mock_file.return_value.__iter__ = lambda x: iter(x.readlines())
            for item in cbs_reader.cbs_reader("1313131"):
                self.assertEqual('N1', item.sample)


if __name__ == '__main__':
    unittest.main()
