using Microsoft.Extensions.Configuration;

namespace PublicApi.Helpers
{
	public static class ConfigurationHelper
	{
		public static string GetDeepLearningUrl(this IConfiguration config) => config["DeepLearningUrl"];
	}
}