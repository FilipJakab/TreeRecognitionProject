namespace PublicApi.Data
{
	// TODO: Move to database and then generate via EF Core
	public class User
	{
		public string UserName { get; set; }
		public string Password { get; set; }

		public bool IsAdmin { get; set; }
	}
}
