# standard library
import datetime
import sys
import unittest

# third party
import mysql.connector

# first party
from delphi.epidata.client.delphi_epidata import Epidata
import delphi.operations.secrets as secrets


class OomTests(unittest.TestCase):

  def setUp(self):
    # connect to the `epidata` database and clear relevant tables
    cnx = mysql.connector.connect(
        user='user',
        password='pass',
        host='delphi_database_epidata',
        database='epidata')
    cur = cnx.cursor()
    # cur.execute('truncate table covidcast')
    # cnx.commit()
    # cur.close()

    # make connection and cursor available to test cases
    self.cnx = cnx
    self.cur = cnx.cursor()

    # use the local instance of the Epidata API
    Epidata.BASE_URL = 'http://delphi_web_epidata/epidata/api.php'

    # use the local instance of the epidata database
    secrets.db.host = 'delphi_database_epidata'
    secrets.db.epi = ('user', 'pass')

  def tearDown(self):
    """Perform per-test teardown."""
    self.cur.close()
    self.cnx.close()

  def test_oom(self):
    """Don't oom with a huge dataset."""

    # insert dummy data
    # num = 0
    # for j in range(1000):
    #   print(datetime.datetime.now())
    #   print(f'batch {j}/1000')
    #   sys.stdout.flush()
    #   for i in range(25000):
    #     self.cur.execute('''
    #       insert into covidcast values
    #         (0, 'src', 'sig', 'day', 'county', %d, '01234',
    #           345, 6.5, 2.2, 11.5, 678, 0, 20200416, 2, 1, True)
    #     ''' % num)
    #     num += 1
    #   self.cnx.commit()

    # fetch data
    response = Epidata.covidcast(
        'src', 'sig', 'day', 'county', Epidata.range(0, 999999999), '01234')

    # check result
    self.assertEqual(response['result'], 1)
    self.assertEqual(len(response['epidata']), 25000000)
