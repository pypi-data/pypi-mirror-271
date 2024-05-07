import unittest
from lugandalens.prediction import decode_prediction

class TestPredictionFunctions(unittest.TestCase):

    def test_decode_prediction(self):
        pred_label = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]  
        num_to_char = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L'}
        max_label_length = 3
        decoded_text = decode_prediction(pred_label, num_to_char, max_label_length)
        expected_result = [['ABC', 'DEF'], ['GHI', 'JKL']]
        self.assertEqual(decoded_text, expected_result)

if __name__ == '__main__':
    unittest.main()

