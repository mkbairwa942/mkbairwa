
package hotel.management.system;


import java.awt.*;
import java.awt.event.*;
import javax.swing.*;


public class Dashboard extends JFrame{

    public static void main(String[] args) {
        new Dashboard().setVisible(true);
    }
    
    public Dashboard() {
        super("HOTEL MANAGEMENT SYSTEM");
	
        setForeground(Color.CYAN);
        setLayout(null); 

        
        ImageIcon i1 = new ImageIcon(ClassLoader.getSystemResource("icons/third.jpg"));
        Image i2 = i1.getImage().getScaledInstance(1900, 1000,Image.SCALE_DEFAULT);
        ImageIcon i3 = new ImageIcon(i2); 
	JLabel NewLabel = new JLabel(i3);
	NewLabel.setBounds(0, 0, 1900, 1000); 
        add(NewLabel);
        
        JLabel HotelSystem = new JLabel("THE TAJ GROUP WELCOMES YOU");
	HotelSystem.setForeground(Color.MAGENTA);
        HotelSystem.setFont(new Font("Tahoma", Font.PLAIN, 46));
	HotelSystem.setBounds(450, 50, 1000, 85);
	NewLabel.add(HotelSystem);
		
		
        JMenuBar menuBar = new JMenuBar();
	setJMenuBar(menuBar);
		
        JMenu HOTEL_MANAGEMENT = new JMenu("HOTEL MANAGEMENT");
        HOTEL_MANAGEMENT.setForeground(Color.BLUE);
	menuBar.add(HOTEL_MANAGEMENT);
		
        JMenuItem RECEPTION = new JMenuItem("RECEPTION");
	HOTEL_MANAGEMENT.add(RECEPTION);
        RECEPTION.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae){
                new Reception();
            }
	});
		
	JMenu ADMIN = new JMenu("ADMIN");
        ADMIN.setForeground(Color.RED);
	menuBar.add(ADMIN);
        
        JMenuItem ADD_EMPLOYEE = new JMenuItem("ADD EMPLOYEE");
	ADMIN.add(ADD_EMPLOYEE);        
        ADD_EMPLOYEE.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae){
                try{
                    new AddEmployee().setVisible(true);
                }catch(Exception e ){}
            }
	});    

        JMenuItem ADD_ROOMS = new JMenuItem("ADD ROOMS");
	ADMIN.add(ADD_ROOMS);        
        ADD_ROOMS.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae){
                try{
                    new AddRoom().setVisible(true);
                }catch(Exception e ){}
            }
	});
         
        JMenuItem ADD_DRIVERS = new JMenuItem("ADD DRIVERS");
	ADMIN.add(ADD_DRIVERS);
	ADD_DRIVERS.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ae){
                try{
                    new AddDrivers().setVisible(true);
                }catch(Exception e ){}
            }
	});
        
		
        setSize(1900,1090);
	setVisible(true);
        getContentPane().setBackground(Color.WHITE);
    }
}