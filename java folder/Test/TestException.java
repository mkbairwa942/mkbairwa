import java.util.*;

class TestException
{
    public static void main(String args[])
    {
        int a,b,c;
        Scanner scan = new Scanner(System.in);
        System.out.print("Enter Two numbers : ");
        a=scan.nextInt();
        b=scan.nextInt();
        try
        {
        c=a/b;
        System.out.println("Divide of "+a+" and "+b+" is :"+c);
        }
        catch(Exception e)
        {System.out.println("Division error");}
        c=a*b;
        System.out.println("Multiply of "+a+" and "+b+" is :"+c);
        c=a+b;
        System.out.println("Addition of "+a+" and "+b+" is :"+c);
        c=a-b;
        System.out.println("Substraction of "+a+" and "+b+" is :"+c);

    }
}