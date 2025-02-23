class MyThread extends Thread
{
    public void run()
    {
        System.out.println("My Thread Starts");
    try
    {
        for(int i=1;i<=10;i++)
        {
        System.out.println(i);
        Thread.sleep(500);
        }
        System.out.println("My Thread Ends");
    }
    catch(InterruptedException e)
    {
        System.out.println(e);
    }
}
}
class TestMultiThreading
{
    public static void main(String args[]) throws InterruptedException
    {
        System.out.println("Main Thread Starts");
        MyThread M1 = new MyThread();
        M1.start();
        System.out.println(M1.isAlive());
        M1.join();
        System.out.println(M1.isAlive());
        System.out.println("Main Thread Ends");
    }
}
