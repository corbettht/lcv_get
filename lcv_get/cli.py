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
@click.option('--num', '-n', default=1000, type=float, help="Max number of stars") 
@click.option('--outname', '-o', default=None, type=str, help="Output directory name")
def cli(ra, dec, verbose, radius, num, outname): 
    import psycopg2 
    import numpy as np
    import psycopg2
    import os
    import sys
 
    cwd = os.getcwd() 
    sys.path.insert(0, cwd)
    try:
        from dbconfig import host, username, password
    except ImportError:
        host = click.prompt('Host')
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True) 
    
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
                  'NUM': num,
                  'RADIUS': radius}

    c.execute(""" SELECT lcv_apassid,
                         sysremepoch,
                         sysrem,
                         sysremerr,
                         sysrem_flags,
                         raj2000,
                         decj2000
                  FROM lcvs
                  WHERE  q3c_radial_query(raj2000,
                                          decj2000,
                                          %(RA)s,
                                          %(DEC)s,
                                          %(RADIUS)s)
                  ORDER BY q3c_dist(raj2000,
                                    decj2000,
                                    %(RA)s,
                                    %(DEC)s) ASC
                  LIMIT %(NUM)s""", query_dict)
    dat = c.fetchall()
    targ = str(dat[0][0])
    if outname:
        targ = outname
    os.system('mkdir ' + targ)
    print(len(dat))
    if len(dat) > 0: 
        for i,src in enumerate(dat):
            source_id = src[0]
            src = np.array(src[1:])
            mjd = src[0]
            mag = src[1]
            magerr = src[2]
            flags = src[3]
            raj2000 = str(src[4])
            decj2000 = str(src[5])
            
            if i ==0:
               np.savetxt(os.path.join(targ, 'EVRTARG_' + str(source_id) + '_'+ raj2000 + '_' + decj2000 + '.csv'), np.c_[mjd, mag, magerr, flags], fmt='%5.8f')
            else:
                np.savetxt(os.path.join(targ, 'EVR_' + str(source_id) + '_'+ raj2000 + '_' + decj2000 + '.csv'), np.c_[mjd, mag, magerr, flags], fmt='%5.8f')
    
    c.close()
    conn.close()

