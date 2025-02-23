// package hotel.management.system;
import java.sql.*;  

public class conn{
    Connection c;
    Statement s;
    public conn(){  
        try{  
            Class.forName("com.mysql.jdbc.Driver");  
            c =DriverManager.getConnection("jdbc:mysql://localhost/hotelmanagementsystem","root",""); 
            System.out.println("DB CONNECTED!");
            
            s =c.createStatement();  
            
           
        }catch(Exception e){ 
            System.out.println("SQL ERROR IS"+e);
        }  
    }  
}  