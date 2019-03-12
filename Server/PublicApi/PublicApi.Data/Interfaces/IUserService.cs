using System.Collections.Generic;

namespace PublicApi.Data.Interfaces
{
	public interface IUserService
	{
		User Authenticate(string username, string password);

		List<User> GetAllUsers();
	}
}
