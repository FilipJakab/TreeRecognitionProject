using System.IO;
using System.Net;
using System.Threading.Tasks;
using PublicApi.Providers;

namespace PublicApi.Managers
{
	public class ImageManager
	{
		public void GetPredictionsForImage(string url, Stream imageStream)
		{
			HttpProvider httpProvider = new HttpProvider();

			Task<WebResponse> response = httpProvider.PostStream(url, imageStream);


		}
	}
}