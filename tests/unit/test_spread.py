from random import randint
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from models.datastore.spread_ds import SpreadModel
from models.spread import Spread


class TestSpread(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        self.year = 2014
        self.week = randint(1, 17)
        self.expected_count = randint(2, 16)

    def tearDown(self):
        self.testbed.deactivate()

    def _generate_data(self, year=2014, week=0, count=1):
        game_id = randint(1000, 9000)
        result = []

        for i in range(count):
            data = {
                'game_id': game_id+i,
                'game_line': randint(35, 55) + 0.5,
                'game_odds': randint(-7, 7) + 0.5,
                'week': week,
                'year': year
            }
            result.append(data)

        return result

    def _prepopulate_datastore(self, year=1990, week=0, count=1):
        ancestor_key = Spread()._generate_key(year=year, week=week)
        data = self._generate_data(year=year, week=week, count=count)

        games = []
        for game in data:
            # Decorate data with ancestor key
            spread_data = {
                'parent': ancestor_key
            }
            spread_data.update(game)
            games.append(SpreadModel(**spread_data))

        ndb.put_multi(entities=games)
        return data

    def test_generate_key(self):
        expected_key = ndb.Key('year', self.year, 'week', self.week)
        key = Spread()._generate_key(year=self.year, week=self.week)
        self.assertEqual(key, expected_key)

    def test_save_spread(self):
        year = 2014
        week = randint(1, 17)
        expected_count = 1
        test_data = self._generate_data(year=year, week=week, count=expected_count)

        spread = Spread()
        count = spread.save(year=year, week=week, data=test_data)
        self.assertEqual(count, expected_count)

        # Check datastore
        ancestor_key = spread._generate_key(year=year, week=week)
        data = SpreadModel().query(ancestor=ancestor_key).order(SpreadModel.game_id).fetch(expected_count+1)
        self.assertEqual(len(data), expected_count)

        for index in range(expected_count):
            expected_game = test_data[index]
            game = data[index].to_dict()
            self.assertEqual(game, expected_game)

    def test_save_multiple_spread(self):
        expected_count = randint(2, 16)
        test_data = self._generate_data(year=self.year, week=self.week, count=expected_count)

        spread = Spread()
        count = spread.save(year=self.year, week=self.week, data=test_data)
        self.assertEqual(count, expected_count)

        # Check datastore
        ancestor_key = spread._generate_key(year=self.year, week=self.week)
        data = SpreadModel().query(ancestor=ancestor_key).order(SpreadModel.game_id).fetch(expected_count+1)
        self.assertEqual(len(data), expected_count)

        for index in range(expected_count):
            expected_game = test_data[index]
            game = data[index].to_dict()
            self.assertEqual(game, expected_game)

    def test_fetch_spread(self):
        expected_count = 1
        test_data = self._prepopulate_datastore(year=self.year, week=self.week, count=expected_count)

        spread = Spread()
        data = spread.fetch(year=self.year, week=self.week)
        self.assertEqual(len(data), expected_count)

        for index, game in enumerate(data):
            expected_game = test_data[index]
            self.assertEqual(game, expected_game)

    def test_fetch_multiple_spread(self):
        expected_count = randint(2, 16)
        test_data = self._prepopulate_datastore(year=self.year, week=self.week, count=expected_count)

        spread = Spread()
        data = spread.fetch(year=self.year, week=self.week)
        self.assertEqual(len(data), expected_count)

        for index, game in enumerate(data):
            expected_game = test_data[index]
            self.assertEqual(game, expected_game)

    def test_find_existing_with_all_data(self):
        test_data = self._prepopulate_datastore(year=self.year, week=self.week, count=self.expected_count)

        spread = Spread()
        key = spread._generate_key(year=self.year, week=self.week)
        data = spread._find_existing_entries(key, test_data)
        self.assertEqual(len(data), self.expected_count)

        for game in test_data:
            self.assertTrue(game['game_id'] in data)

    def test_find_existing_with_some_data(self):
        test_data = self._generate_data(year=self.year, week=self.week, count=self.expected_count)
        spread = Spread()
        key = spread._generate_key(year=self.year, week=self.week)

        # Preload half
        preload = []
        preload_count = self.expected_count/2
        for i in range(preload_count):
            spread_data = {'parent': key}
            spread_data.update(test_data[i])
            preload.append(SpreadModel(**spread_data))
        ndb.put_multi(preload)

        data = spread._find_existing_entries(key, test_data)
        self.assertEqual(len(data), preload_count)

        for game in preload:
            self.assertTrue(game.game_id in data)

    def test_update_model(self):
        generated_data = self._generate_data(year=self.year, week=self.week, count=1)
        test_data = generated_data[0]

        model = SpreadModel(**test_data)
        test_data['game_line'] += randint(1, 100)

        spread = Spread()
        result = spread._update_model(model, test_data)
        self.assertEqual(result.to_dict(), test_data)

    def test_save_same(self):
        expected_count = 1
        generated_data = self._generate_data(year=self.year, week=self.week, count=expected_count)

        spread = Spread()
        count = spread.save(year=self.year, week=self.week, data=generated_data)

        generated_data[0]['game_line'] += 13
        count = spread.save(year=self.year, week=self.week, data=generated_data)

        # Check datastore
        ancestor_key = spread._generate_key(year=self.year, week=self.week)
        data = SpreadModel().query(ancestor=ancestor_key).fetch(expected_count+1)
        self.assertEqual(len(data), expected_count)

        for index in range(expected_count):
            expected_game = generated_data[index]
            game = data[index].to_dict()
            self.assertEqual(game, expected_game)

    def test_fetch_by_id(self):
        expected_count = 1
        generated_data = self._prepopulate_datastore(year=self.year, week=self.week)
        test_data = generated_data[0]

        spread = Spread()
        data = spread.fetch_by_id(year=self.year, week=self.week, game_id=test_data['game_id'])
        self.assertEqual(data, test_data)

    def test_save_by_id(self):
        generated_data = self._generate_data(year=self.year, week=self.week)
        test_data = generated_data[0]
        game_id = test_data['game_id']

        spread = Spread()
        count = spread.save_by_id(year=self.year, week=self.week, game_id=game_id, data=test_data)
        self.assertEqual(count, 1)

        # Check datastore
        data = SpreadModel.query(SpreadModel.game_id == game_id).fetch(1)
        self.assertEqual(data[0].to_dict(), test_data)

    def test_save_by_id_same(self):
        generated_data = self._generate_data(year=self.year, week=self.week)
        test_data = generated_data[0]
        game_id = test_data['game_id']

        spread = Spread()
        spread.save_by_id(year=self.year, week=self.week, game_id=game_id, data=test_data)

        test_data['game_line'] += randint(7, 14)
        spread.save_by_id(year=self.year, week=self.week, game_id=game_id, data=test_data)

        # Check datastore
        data = SpreadModel.query(SpreadModel.game_id == game_id).fetch(2)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].to_dict(), test_data)
