abstract class Area
{
    abstract void area();
}

class Circle extends Area
{
    void area()
    {
        double r =12.44,A,PI=3.14;
        A=PI*r*r;
        System.out.println("Area of Circle Abstracrt is :"+A);
    }
}

class Rect extends Area
{
    void area()
    {
        double l=10.5,w=20.4,A;
        A=l*w;
        System.out.println("Area of Rect Abstracrt is :"+A);
    }
}

class TestAbstract
{
    public static void main(String args[])
    {
        Area A=new Rect();
        Area B=new Circle();
        A.area();
        B.area();
    }
}