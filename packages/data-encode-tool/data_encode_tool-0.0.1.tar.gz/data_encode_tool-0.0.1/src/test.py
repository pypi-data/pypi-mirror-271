import unittest
import data_encode_tool

class MyTest(unittest.TestCase):

    def test_number(self):
        num = "3.1415926414156784352453565634"
        data = data_encode_tool.encode_u40(num)
        ret = data_encode_tool.decode_u40(data)
        self.assertEqual(num, ret)

        num = "01234567890123"
        data = data_encode_tool.encode_u40(num)
        ret = data_encode_tool.decode_u40(data)
        self.assertEqual(num, ret)

    def test_gene(self):
        
        gene = "ATCGGGGTTAAACCCCATCGGGGTTAAACCCC"
        data = data_encode_tool.encode_gene(gene)
        ret = data_encode_tool.decode_gene(data)
        self.assertEqual(gene, ret)

        gene = "ATCG"
        data = data_encode_tool.encode_gene(gene)
        ret = data_encode_tool.decode_gene(data)
        self.assertEqual(gene, ret)


        gene = "ATCGA"
        data = data_encode_tool.encode_gene(gene)
        ret = data_encode_tool.decode_gene(data)
        self.assertEqual(gene, ret)


if __name__ == '__main__':
    unittest.main()