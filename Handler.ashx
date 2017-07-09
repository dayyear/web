<%@ WebHandler Language="C#" Class="Handler" %>

using System;
using System.Configuration;
using System.Data.SqlClient;
using System.Data.SQLite;
using System.Web;

public class Handler : IHttpHandler
{

    public void ProcessRequest(HttpContext context)
    {
        var Server = context.Server;
        var Response = context.Response;
        
        Response.ContentType = "text/plain";
        //Response.Write("Hello World");

        using (var cn = new SQLiteConnection("Data Source=" + Server.MapPath(ConfigurationManager.ConnectionStrings["web"].ConnectionString)))
        {
            cn.Open();
            using (var cmd = cn.CreateCommand())
            {
                cmd.CommandText = "select * from person limit 0, 10";
                using (var dr = cmd.ExecuteReader())
                {
                    while (dr.Read())
                    {
                        for (int col = 0; col < dr.FieldCount; col++)
                        {
                            string field = dr.GetName(col);
                            string value = dr[col].ToString();
                            Response.Write(string.Format("{0}: {1}{2}", field, value, Environment.NewLine));
                        }//for (int col = 0; col < dr.FieldCount; col++)
                        Response.Write(Environment.NewLine);
                    }//while (dr.Read())
                }//dr
            }//cmd
        }//cn

    }

    public bool IsReusable
    {
        get
        {
            return false;
        }
    }

}