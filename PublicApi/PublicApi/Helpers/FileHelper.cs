using System;
using System.IO;

namespace PublicApi.Helpers
{
	public static class FileHelper
	{
		public static string GetNewFileName(string folder, string extension)
		{
			return Path.Join(folder, $"{Guid.NewGuid()}{extension}");
		}
	}
}
