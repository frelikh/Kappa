Notes...

1. Make a list of all of the .kappa files: ls > list_of_maps.txt
2. make_kappa_list.py takes the list_of_maps.txt and uses that to
   turn the .kappa files to .fits files, which is needed for the
   pangloss code to work
3. Now, make a list of the .fits files and call that list_of_fits.txt
   ls *.fits > list_of_fits.txt
4. Now you can run kappa_vals.py to make a bunch of KappasByCenter

   -> make sure to change indir, depending on which plane number you're doing
   In the KappasByCenter folder, the text files are numbered as follows:
   kappasij_mn.txt, where:
      i - column number on 4x4 degree field, going from left to right, 0 to 3
      j - row number on 4x4 degree fields, going from bottom to top, 0 to 3

      Since there are 32 files in this case (4x8 = 32)
      m - index going from 0 to 3
      n - index going from 0 to 7
         * m and n are just indeces to keep track of which simulated
	 * field we're talking about - they have nothing to do with
	 * actual coordinates on the grid!

5. Now that you have the kappas, all you have to do is find which
   lines of sight from the simulation roughly match your number count,
   and look up the kappa values for those lines of sight in the
   KappasByCenter files

   This is done by make_kappa_hist.py.

   In the make_kappa_hist.py file, you need to specify:
      - i range - this usually will be from 0 to 3 - this is the m index in kappasij_mn.txt
      - j range - this usually will be from 0 to 7 - this is the n index in kappasij_mn.txt

      - k and l range should be fine

      - the tables with the number counts should be the same because that's just all the simulation
      	data, I think

      - make sure you change the kappa_dir path to match whichever plane number you have

6. Yay you're done! Delete the fits files created in (2.) to save space.
   rm GGL*.fits
