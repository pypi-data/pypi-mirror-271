import unittest
from collections import ChainMap
from pathlib import Path

from libsrg.Config import Config

dir_path: Path = Path(__file__).parent

d1 = {"x": "xray", "y": "yray", "z": "zray", "id": "d1","d1":1}  # AI for the win
d2 = {"xx": "{{x}}", "yy": "yankee", "zz": "zulu", "id": "d2","d2":2}
d3 = {"xx": "{{x}}", "yy": "yankee", "zz": "zulu", "id": "d3","d3":3}
d4 = {"xx": "{{x}}", "yy": "yankee", "zz": "zulu", "id": "d4","d4":4}
d5 = {"xx": "{{x}}", "yy": "yankee", "zz": "zulu", "id": "d5","d5":5}


class MyTestCase(unittest.TestCase):
    def test_process_args_dicts(self):
        # first make sure dicts pass
        out = Config.process_args(d1, d2)
        self.assertEqual([d1, d2], out)  # add assertion here

    def test_process_args_chainmap(self):
        # check breakdown of ChainMap
        out = Config.process_args(d1, d2)
        self.assertEqual([d1, d2], out)  # add assertion here

    def test_process_args_path(self):
        # check load from path variable
        sp = dir_path / 'Sample.json'
        out = Config.process_args(sp)
        self.assertEqual(1, len(out))
        d = out[0]
        self.assertTrue(isinstance(d, dict))
        self.assertEqual("apple", d["a"])

    def test_process_args_filename_json(self):
        # check load from string filename
        sp = dir_path / 'Sample.json'
        out = Config.process_args(str(sp))
        self.assertEqual(1, len(out))
        d = out[0]
        self.assertTrue(isinstance(d, dict))
        self.assertEqual("apple", d["a"])

    def test_process_args_filename_env(self):
        # check load from string filename
        sp = dir_path / 'Sample.env'
        out = Config.process_args(str(sp))
        self.assertEqual(1, len(out))
        d = out[0]
        self.assertTrue(isinstance(d, dict))
        self.assertEqual("apple", d["a"])

    def test_process_args_filename_ini(self):
        # check load from string filename
        sp = dir_path / 'Sample.ini'
        out = Config.process_args(str(sp))
        self.assertEqual(1, len(out))
        d = out[0]
        self.assertTrue(isinstance(d, dict))
        self.assertTrue("sect1" in d)
        s1 = d["sect1"]
        self.assertTrue(isinstance(s1, dict))
        self.assertEqual("apple", s1["a"])

    def test_constructor_filename_json(self):
        sp = dir_path / 'Sample.json'
        cf = Config(sp)
        self.assertTrue(isinstance(cf, Config))
        self.assertTrue(isinstance(cf, ChainMap))
        self.assertEqual("apple", cf["a"])

    def test_copy_and_new_child(self):
        sp = dir_path / 'Sample.json'
        cf = Config(sp)

        # verifying that these return the proper subclass
        cf2 = cf.copy()
        self.assertTrue(isinstance(cf2, Config))
        # noinspection PyArgumentList
        cf3 = cf.new_child(a="alpha")
        self.assertEqual("alpha", cf3["a"])
        self.assertTrue(isinstance(cf3, Config))

    def test_secrets(self):
        cfs = Config(d2)
        cf = Config(d1)
        self.assertEqual("xray", cf.get_item("x", default="QQQ"))
        self.assertEqual("QQQ", cf.get_item("yy", default="QQQ"))
        self.assertEqual("QQQ", cf.get_item("yy", default="QQQ", secrets=True))

        Config.set_secrets(cfs)
        self.assertEqual("xray", cf.get_item("x", default="QQQ"))
        self.assertEqual("QQQ", cf.get_item("yy", default="QQQ"))
        self.assertEqual("yankee", cf.get_item("yy", default="QQQ", secrets=True))
        self.assertEqual("xray", cf.get_item("xx", default="QQQ", secrets=True))

    def test_order(self):
        c123 = Config(d1, d2, d3)
        ids = self.print_ids(c123)
        self.assertEqual(["d1", "d2", "d3"], ids)
        self.assertEqual([d1, d2, d3], c123.maps)

        c4 = Config(d4, c123)
        ids = self.print_ids(c4)
        self.assertEqual(["d4", "d1", "d2", "d3"], ids)
        self.assertEqual([d4, d1, d2, d3], c4.maps)

        c4 = Config(c123, d4)
        ids = self.print_ids(c4)
        self.assertEqual(["d1", "d2", "d3", "d4"], ids)
        self.assertEqual([d1, d2, d3, d4], c4.maps)

        c45 = Config(d4, d5)
        ids = self.print_ids(c45)
        self.assertEqual(["d4", "d5"], ids)

        self.assertEqual([d4, d5], c45.maps)
        c15 = Config(c123, c45)
        ids = self.print_ids(c15)
        self.assertEqual(["d1", "d2", "d3", "d4", "d5"], ids)
        self.assertEqual([d1, d2, d3, d4, d5], c15.maps)

    # noinspection PyMethodMayBeStatic
    def print_ids(self, x: Config):
        ids = [m.get("id", "XX") for m in x.maps]
        print(ids)
        return ids

    def test_find_item_depth(self):
        c= Config(d1,d2,d3,d4,d5)

        d,v= c.find_item_depth("d1")
        self.assertEqual(0,d)
        self.assertEqual(1,v)

        d,v= c.find_item_depth("d2")
        self.assertEqual(1,d)
        self.assertEqual(2,v)

        d,v= c.find_item_depth("d3")
        self.assertEqual(2,d)
        self.assertEqual(3,v)

        d,v= c.find_item_depth("d4")
        self.assertEqual(3,d)
        self.assertEqual(4,v)

        d,v= c.find_item_depth("d5")
        self.assertEqual(4,d)
        self.assertEqual(5,v)

        d,v= c.find_item_depth("d6")
        self.assertEqual(None,d)
        self.assertEqual(None,v)

    def test_save_load(self):
        c= Config(d1,d2,d3,d4,d5)
        c.to_json_file("/tmp/test.json")
        c2 = Config("/tmp/test.json")
        self.assertEqual(c.to_flat_dict(), c2.to_flat_dict())

if __name__ == '__main__':
    unittest.main()
