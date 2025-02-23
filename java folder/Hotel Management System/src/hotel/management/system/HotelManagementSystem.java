package hotel.management.system;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class HotelManagementSystem extends JFrame implements ActionListener{

        JLabel l1;
        JButton b1;
        
        public HotelManagementSystem() {
		
                setSize(1366,600);          // setContentPane(300,300,1366,390);   frame size
                setLayout(null);
                setLocation(100,100);
                // setVisible(true);

		l1 = new JLabel("");
                b1 = new JButton("NEXT");
                
                b1.setBackground(Color.GREEN);
                b1.setForeground(Color.BLACK);	
                b1.setFont(new Font("serif",Font.BOLD,30));               
                
                ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/first.jpg"));
                // D:\STOCK\Capital_vercel_new\java folder\HotelManagementSystem\src\icons\first.jpg

                Image i3 = i1.getImage().getScaledInstance(1366, 600,Image.SCALE_DEFAULT);
                ImageIcon i2 = new ImageIcon(i3);
                l1 = new JLabel(i2);
                
                JLabel lid=new JLabel("HOTEL MANAGEMENT SYSTEM");
                lid.setBounds(30,460,1500,100);
                lid.setFont(new Font("serif",Font.PLAIN,70));
                lid.setForeground(Color.red);
                l1.add(lid);
                
                b1.setBounds(1170,490,150,50);
		l1.setBounds(0, 0, 1366, 600);
                
                l1.add(b1);
		add(l1);
 
                b1.addActionListener(this);
                setVisible(true);
                
                while(true){
                        lid.setVisible(false); // lid =  j label
                    try{
                        Thread.sleep(500); //1000 = 1 second
                    }catch(Exception e){} 
                        lid.setVisible(true);
                    try{
                        Thread.sleep(500);
                    }catch(Exception e){}
                }
	}
        
        public void actionPerformed(ActionEvent ae){
                new Login().setVisible(true);
                this.setVisible(false);
                
        }
        
        public static void main(String[] args) {
                HotelManagementSystem window = new HotelManagementSystem();
                window.setVisible(true);			
	}
}