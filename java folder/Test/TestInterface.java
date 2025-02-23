interface Area
{
    double PI=3.14;
    void area();
}

class Circle implements Area
{
    public void area()
    {
        double r =12.44,A,PI=3.14;
        A=PI*r*r;
        System.out.println("Area of Circle interface is :"+A);
    }
}

class Rect implements Area
{
    public void area()
    {
        double l=10.5,w=20.4,A;
        A=l*w;
        System.out.println("Area of Rect interface is :"+A);
    }
}

class TestInterface
{
    public static void main(String args[])
    {
        Area A=new Rect();
        Area B=new Circle();
        A.area();
        B.area();
    }
}