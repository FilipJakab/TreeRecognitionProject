using System.IO;
using System.Net;
using System.Threading.Tasks;

namespace PublicApi.Providers
{
	public class HttpProvider
	{
		public Task<WebResponse> PostStream(string url, Stream content)
		{
			HttpWebRequest request = WebRequest.CreateHttp(url);

			request.Method = WebRequestMethods.Http.Post;
			return request.GetResponseAsync();
		}
	}
}