#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: lcv_get.cli
.. moduleauthor:: hank corbett <my_email>

This is the entry point for the command-line interface (CLI) application.  It
can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.
"""
import logging
import click
from .__init__ import __version__

# Change the options to below to suit the actual options for your task (or
# tasks).
@click.command()
@click.argument('RA', type=float)
@click.argument('DEC', type=float)
@click.option('--verbose', '-v', is_flag=True, default=False, help="Enable verbose output.")
@click.option('--radius', '-r', default=(26./3600.), type=float, help="Radius for cone search") 
def cli(ra, dec, verbose, radius): 
    import psycopg2 
    import numpy as np
    import psycopg2
    import os
 
    if not os.path.isfile('./dbconfig.py'):
        host = click.prompt('Host')
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True) 
    else:
        from .dbconfig import host, username, password
    
    conn_string = "host='" + host + "' "\
                  "dbname='apphot_pipeline' "\
                  "user='" + username + "' "\
                  "password='" + password +"' "\
                  "port='4352'" 
    conn = psycopg2.connect(conn_string)
    conn.set_client_encoding('UTF8')
    
    c = conn.cursor()

    query_dict = {'RA': ra,
                  'DEC': dec,
                  'RADIUS': radius}

    c.execute(""" SELECT lcv_apassid,
                         sysremepoch,
                         sysrem,
                         sysremerr
                  FROM lcvs
                  WHERE  q3c_radial_query(raj2000,
                                          decj2000,
                                          %(RA)s,
                                          %(DEC)s,
                                          %(RADIUS)s)
                  ORDER BY catmag
                  LIMIT 1""", query_dict)
    dat = c.fetchall()[0]
    if len(dat) > 0: 
        source_id = dat[0]
        dat = np.array(dat[1:])
        mjd = dat[0]
        mag = dat[1]
        magerr = dat[2]

        np.savetxt('EVR_' + str(source_id) + '.csv', np.c_[mjd, mag, magerr], fmt='%5.8f')
    
    c.close()
    conn.close()

