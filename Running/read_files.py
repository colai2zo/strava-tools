import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import collections.abc
collections.Iterable = collections.abc.Iterable
import gpxpy
import gpxpy.gpx

GPXDIR = "./user-data"


def read_gpx_files():

	bad_files = []
	activity = []
	activity_type = []
	name = []
	latitude = []
	longitude = []
	elevation = []
	timestamp = []

	gpx_files = os.listdir(GPXDIR)
	for i in range(len(gpx_files)):
		
		print("Reading file", i + 1, "of", len(gpx_files))
		try:
			filepath = os.path.join(GPXDIR, gpx_files[i])
			gpx_file = open(filepath, "r", encoding = "utf8")
			gpx_data = gpxpy.parse(gpx_file)
		except:
			bad_files.append(filepath)
			pass

		for track in gpx_data.tracks:
			for segment in track.segments:
				for point in segment.points:
					activity.append("gpx_" + str(i))
					activity_type.append(track.type)
					name.append(track.name)
					latitude.append(point.latitude)
					longitude.append(point.longitude)
					elevation.append(point.elevation)
					timestamp.append(point.time)

	print(len(set(activity)), "files read.", len(bad_files),
		"files are bad.", len(gpx_files)-(len(set(activity))+len(bad_files)),
		"are not gpx files.")

	return bad_files, activity, activity_type, name, latitude, longitude, elevation, timestamp


def main():
	gpx_bad_files, gpx_activity, gpx_activity_type, gpx_name, gpx_latitude, gpx_longitude, gpx_elevation, gpx_timestamp = read_gpx_files()

	gpx_df = pd.DataFrame(
		list(zip(gpx_timestamp, gpx_activity, gpx_activity_type, gpx_name, gpx_latitude, gpx_longitude, gpx_elevation)),
		columns = ["Time", "Activity", "Type", "Name", "Latitude", "Longitude", "Elevation"]
		)

	gpx_df.to_pickle("gpx.pkl")


if __name__ == '__main__':
	main()