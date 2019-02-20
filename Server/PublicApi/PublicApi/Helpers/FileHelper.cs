using System;
using System.IO;

namespace PublicApi.Helpers
{
	public static class FileHelper
	{
		/// <summary>
		/// Retrieve new Guid-based FileName with given extension at given folder
		/// </summary>
		/// <param name="folder"></param>
		/// <param name="extension"></param>
		/// <returns>Joined path in format: "<paramref name="folder"/>/NEW_GUID.<paramref name="extension"/>"</returns>
		public static string GetNewFileName(string folder, string extension)
		{
			return Path.Join(folder, $"{Guid.NewGuid()}{extension}");
		}
	}
}
