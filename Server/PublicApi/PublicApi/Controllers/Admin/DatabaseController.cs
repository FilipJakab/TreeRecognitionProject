using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PublicApi.Database;
using PublicApi.ReflectionHelpers;

namespace PublicApi.Controllers.Admin
{
	/// <summary>
	/// Serves as API endpoint which should return 'raw' data (for example from database)
	/// </summary>
	[Route("api/admin/database")]
	[EnableCors("AllowedOriginsPolicy")]
	public class DatabaseController : ControllerBase
	{
		private List<PropertyInfo> getContextProperties;
		private readonly ILogger<DatabaseController> logger;
		private readonly TreeRecognitionDbContext context;
		private readonly DbContextReflectionHelper reflectionHelper;
		
		private List<PropertyInfo> contextProperties =>
			getContextProperties ?? (getContextProperties = context
				.GetType()
				.GetProperties()
				.Where(prop => prop.PropertyType.IsGenericType &&
				               prop.PropertyType == typeof(DbSet<>).MakeGenericType(prop.PropertyType.GenericTypeArguments))
				.ToList());


		public DatabaseController(ILogger<DatabaseController> logger, TreeRecognitionDbContext context)
		{
			this.logger = logger;
			this.context = context;
			
			// context.WebRequest.TL
			
			reflectionHelper = new DbContextReflectionHelper();
		}

		[HttpGet("gettables")]
		public IActionResult GetTables()
		{
			List<string> tableNames = new List<string>();

			foreach (PropertyInfo property in contextProperties)
			{
				string name = property.Name,
					nameLower = property.Name.ToLower();
				if (nameLower.EndsWith("dbcontext") || nameLower == "model" || nameLower == "database" ||
				    nameLower == "changetracker")
					continue;

				tableNames.Add(name);
			}

			return Ok(tableNames);
		}

		[HttpGet("{tableName}/data")]
		public IActionResult GetTableData([FromRoute] string tableName, [FromQuery] int top = 25)
		{
			PropertyInfo requestedTableProperty = contextProperties.FirstOrDefault(field =>
				field.Name.ToLower().Equals(tableName.ToLower()));

			if (requestedTableProperty == null)
				return NotFound("Table was not found");
			
			// context.WebRequest.Take()

			object payload = requestedTableProperty.GetValue(context);

			// payload = reflectionHelper.Take(payload, top);
			
			return Ok(reflectionHelper.ToList(payload));
		}

		// Not working
		// [HttpDelete("{tableName}")]
		// public IActionResult Delete([FromRoute] string tableName, [FromBody] string keyColumnName, [FromBody] object key)	
		// {
		// 	PropertyInfo requestedTableProperty = contextProperties.FirstOrDefault(field =>
		// 		field.Name.ToLower().Equals(tableName.ToLower()));
		// 	
		// 	if (requestedTableProperty == null)
		// 		return NotFound("Table was not found");
		//
		// 	PropertyInfo tableKeyColumnInfo = requestedTableProperty.PropertyType.GenericTypeArguments.First()
		// 		.GetProperties()
		// 		.FirstOrDefault(prop => prop.Name.ToLower().Equals(keyColumnName));
		//
		// 	object table = requestedTableProperty.GetValue(context);
		// 	object found = reflectionHelper.Where(table, tableRow => tableKeyColumnInfo.GetValue(tableRow) == key);
		//
		// 	return Ok(found);
		// }
	}
}
