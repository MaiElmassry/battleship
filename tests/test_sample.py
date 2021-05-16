import unittest
import json
import requests

base = "http://127.0.0.1:5000/battleship"


class TestSampleClass(unittest.TestCase):

    def test_success_create_game(self):
        requests.delete(base)
        success_payload = json.dumps({
            "ships": [
                {
                    "x": 2,
                    "y": 1,
                    "size": 4,
                    "direction": "H"
                },
                {
                    "x": 7,
                    "y": 4,
                    "size": 3,
                    "direction": "V"
                },
                {
                    "x": 3,
                    "y": 5,
                    "size": 2,
                    "direction": "V"
                },
                {
                    "x": 6,
                    "y": 8,
                    "size": 1,
                    "direction": "H"
                }
            ]
        })
        suce_response = requests.post(base, headers={"Content-Type": "application/json"}, data=success_payload)
        self.assertEqual(200, suce_response.status_code)

    def test_overlap_ship(self):
        requests.delete(base)
        over_lap_payload = json.dumps({
            "ships": [
                {
                    "x": 5,
                    "y": 5,
                    "size": 4,
                    "direction": "H"
                },
                {
                    "x": 7,
                    "y": 4,
                    "size": 3,
                    "direction": "V"
                }
            ]
        })
        over_lap_res = requests.post(base, headers={"Content-Type": "application/json"}, data=over_lap_payload)
        self.assertEqual(400, over_lap_res.status_code)

    def test_ship_outside_board(self):
        requests.delete(base)
        over_lap_payload = json.dumps({
            "ships": [
                {
                    "x": 8,
                    "y": 1,
                    "size": 4,
                    "direction": "H"
                }
            ]
        })
        over_lap_res = requests.post(base, headers={"Content-Type": "application/json"}, data=over_lap_payload)
        self.assertEqual(400, over_lap_res.status_code)

    def test_shot_hit(self):
        self.test_success_create_game()
        hit_payload = json.dumps({
            "x": 2,
            "y": 1
        })
        response = requests.put(base, headers={"Content-Type": "application/json"}, data=hit_payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual("HIT", response.json().get("result"))

    def test_shot_sink(self):
        hit_payload = json.dumps({
            "x": 6,
            "y": 8
        })
        response = requests.put(base, headers={"Content-Type": "application/json"}, data=hit_payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual("SINK", response.json().get("result"))

    def test_shot_water(self):
        hit_payload = json.dumps({
            "x": 0,
            "y": 0
        })
        response = requests.put(base, headers={"Content-Type": "application/json"}, data=hit_payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual("WATER", response.json().get("result"))

    def test_shot_fail(self):
        hit_payload = json.dumps({
            "x": 10,
            "y": 0
        })
        response = requests.put(base, headers={"Content-Type": "application/json"}, data=hit_payload)
        self.assertEqual(400, response.status_code)


if __name__ == "__main__":
    unittest.main()
