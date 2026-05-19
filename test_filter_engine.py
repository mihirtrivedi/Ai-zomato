import unittest
import pandas as pd
from filter_engine import apply_filters

class TestFilterEngine(unittest.TestCase):
    def setUp(self):
        # Create a mock dataframe mimicking the structure of our Zomato dataset
        data = {
            'name': ['Cheap Italian', 'Fancy Italian', 'Cheap Chinese', 'Fancy Chinese', 'Mid Italian'],
            'location': ['delhi', 'delhi', 'bangalore', 'bangalore', 'delhi'],
            'cuisine': ['italian', 'italian', 'chinese', 'chinese', 'italian'],
            'cost': [400.0, 2000.0, 300.0, 2500.0, 1000.0],
            'rating': [4.0, 4.8, 3.5, 4.9, 4.5]
        }
        self.df = pd.DataFrame(data)

    def test_city_filter(self):
        result = apply_filters(self.df, city='delhi')
        self.assertEqual(len(result), 3)
        self.assertTrue(all(r['location'] == 'delhi' for r in result))

    def test_cuisine_filter(self):
        result = apply_filters(self.df, cuisine='chinese')
        self.assertEqual(len(result), 2)
        self.assertTrue(all(r['cuisine'] == 'chinese' for r in result))

    def test_budget_filter(self):
        low = apply_filters(self.df, budget='low')
        self.assertEqual(len(low), 2)
        
        medium = apply_filters(self.df, budget='medium')
        self.assertEqual(len(medium), 1)
        self.assertEqual(medium[0]['name'], 'Mid Italian')
        
        high = apply_filters(self.df, budget='high')
        self.assertEqual(len(high), 2)

    def test_combined_filters(self):
        result = apply_filters(self.df, city='delhi', cuisine='italian', budget='high')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Fancy Italian')

    def test_top_n_and_sorting(self):
        result = apply_filters(self.df, city='delhi', cuisine='italian', top_n=2)
        self.assertEqual(len(result), 2)
        # Should be sorted by rating desc
        self.assertEqual(result[0]['name'], 'Fancy Italian') # rating 4.8
        self.assertEqual(result[1]['name'], 'Mid Italian')   # rating 4.5
        
    def test_empty_result(self):
        result = apply_filters(self.df, city='mumbai')
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
