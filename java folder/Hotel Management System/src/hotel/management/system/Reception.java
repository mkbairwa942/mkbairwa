
package hotel.management.system;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Reception extends JFrame {

	private JPanel contentPane;

	public static void main(String[] args) {
		new Reception();
	}
	
	public Reception(){
		
        setBounds(350, 150, 850, 570);
		contentPane = new JPanel();
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/fourth.jpg"));
		Image i3 = i1.getImage().getScaledInstance(500, 500,Image.SCALE_DEFAULT);
		ImageIcon i2 = new ImageIcon(i3);
		JLabel l1 = new JLabel(i2);
		l1.setBounds(300,30,500,470);
		add(l1);
		
		JButton btnNewCustomerForm = new JButton("New Customer Form");
		btnNewCustomerForm.setBounds(50, 30, 200, 30);
        btnNewCustomerForm.setBackground(Color.BLACK);
        btnNewCustomerForm.setForeground(Color.WHITE);
		contentPane.add(btnNewCustomerForm);
		btnNewCustomerForm.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
				NewCustomer custom = new NewCustomer();
				custom.setVisible(true);
                setVisible(false);
			}catch(Exception e1){
				e1.printStackTrace();
			}
			}
		});

		
		JButton btnRoom = new JButton("Room");
		btnRoom.setBounds(50, 70, 200, 30);
		btnRoom.setBackground(Color.BLACK);
		btnRoom.setForeground(Color.WHITE);
		contentPane.add(btnRoom);
		btnRoom.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				try{
				Room room = new Room();
				room.setVisible(true);
                setVisible(false);
				}
				catch(Exception e){
					e.printStackTrace();
				}
				
			}
		});

		
		JButton btnDepartment = new JButton("Department");
		btnDepartment.setBounds(50, 110, 200, 30);
        btnDepartment.setBackground(Color.BLACK);
        btnDepartment.setForeground(Color.WHITE);
		contentPane.add(btnDepartment);
		btnDepartment.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
					Department dept = new Department();
					dept.setVisible(true);
					setVisible(false);
					
				}
				catch (Exception e1){
					e1.printStackTrace();
				}
			
			}
		});

		
		JButton btnAllEmployeeInfo = new JButton("All Employee Info");
		btnAllEmployeeInfo.setBounds(50, 150, 200, 30);                
		btnAllEmployeeInfo.setBackground(Color.BLACK);
		btnAllEmployeeInfo.setForeground(Color.WHITE);
		contentPane.add(btnAllEmployeeInfo);
		btnAllEmployeeInfo.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
				
					Employee em = new Employee();
					em.setVisible(true);
					setVisible(false);
					
				}
				catch (Exception e1){
					e1.printStackTrace();
				}
			
			}
		});

		
		JButton btnCustomerInfo = new JButton("Customer Info");
		btnCustomerInfo.setBounds(50, 190, 200, 30);
		btnCustomerInfo.setBackground(Color.BLACK);
		btnCustomerInfo.setForeground(Color.WHITE);
		contentPane.add(btnCustomerInfo);
		btnCustomerInfo.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
					CustomerInfo customer = new CustomerInfo();
					customer.setVisible(true);				
					setVisible(false);
				}
				catch (Exception e1){
					e1.printStackTrace();
				}
			}
		});

		
		JButton btnManagerInfo = new JButton("Manager Info");
		btnManagerInfo.setBounds(50, 230, 200, 30);
		btnManagerInfo.setBackground(Color.BLACK);
		btnManagerInfo.setForeground(Color.WHITE);
		contentPane.add(btnManagerInfo);
		btnManagerInfo.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
				ManagerInfo mana = new ManagerInfo();
				mana.setVisible(true);
                setVisible(false);
				}
				catch (Exception e1){
					e1.printStackTrace();
				}
			}
		});

		
		JButton btnCheckOut = new JButton("Check Out");
		btnCheckOut.setBounds(50, 270, 200, 30);
		btnCheckOut.setBackground(Color.BLACK);
		btnCheckOut.setForeground(Color.WHITE);
		contentPane.add(btnCheckOut);
		btnCheckOut.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				CheckOut check;
				try {
					check = new CheckOut();
					check.setVisible(true);
                    setVisible(false);
				} catch (Exception e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			}
		});

		
		JButton btnUpdateCheckStatus = new JButton("Update Check Status");
		btnUpdateCheckStatus.setBounds(50, 310, 200, 30);
		btnUpdateCheckStatus.setBackground(Color.BLACK);
		btnUpdateCheckStatus.setForeground(Color.WHITE);
		contentPane.add(btnUpdateCheckStatus);
		btnUpdateCheckStatus.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
				UpdateCheck update = new UpdateCheck();
				update.setVisible(true);
                setVisible(false);
				}
				catch(Exception e1){
					e1.printStackTrace();
				}
			}
		});

		
		JButton btnUpdateRoomStatus = new JButton("Update Room Status");
		btnUpdateRoomStatus.setBounds(50, 350, 200, 30);
		btnUpdateRoomStatus.setBackground(Color.BLACK);
		btnUpdateRoomStatus.setForeground(Color.WHITE);
		contentPane.add(btnUpdateRoomStatus);
		btnUpdateRoomStatus.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try{
					UpdateRoom room = new UpdateRoom();
					room.setVisible(true);
                setVisible(false);
				}catch(Exception s)
				{
					s.printStackTrace();
				}
			}
		});

		
		JButton btnPickUpSerice = new JButton("Pick up Service");
		btnPickUpSerice.setBounds(50, 390, 200, 30);
		btnPickUpSerice.setBackground(Color.BLACK);
		btnPickUpSerice.setForeground(Color.WHITE);
		contentPane.add(btnPickUpSerice);
		btnPickUpSerice.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				try{
				PickUp pick = new PickUp();
				pick.setVisible(true);
                setVisible(false);
				}
				catch(Exception e){
					e.printStackTrace();
				}
			}
		});

		
		JButton btnSearchRoom = new JButton("Search Room");
		btnSearchRoom.setBounds(50, 430, 200, 30);
		btnSearchRoom.setBackground(Color.BLACK);
		btnSearchRoom.setForeground(Color.WHITE);
		contentPane.add(btnSearchRoom);
		btnSearchRoom.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
				SearchRoom search = new SearchRoom();
				search.setVisible(true);
                setVisible(false);
				}
				catch (Exception ss){
					ss.printStackTrace();
				}
			}
		});


		JButton btnLogOut = new JButton("Log Out");
		btnLogOut.setBounds(50, 470, 95, 30);
		btnLogOut.setBackground(Color.BLACK);
		btnLogOut.setForeground(Color.WHITE);
		contentPane.add(btnLogOut);
		btnLogOut.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ae) {
				try {
                new Login().setVisible(true);
                setVisible(false);
                                    
				} catch (Exception e) {
					e.printStackTrace();
				}
				
			}
		});

		JButton btnBack = new JButton("Back");
		btnBack.setBounds(155, 470, 95, 30);
		btnBack.setBackground(Color.BLACK);
		btnBack.setForeground(Color.WHITE);
		contentPane.add(btnBack);
		btnBack.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ae) {
				try {
                new Dashboard().setVisible(true);
                setVisible(false);
                                    
				} catch (Exception e) {
					e.printStackTrace();
				}
				
			}
		});

                getContentPane().setBackground(Color.WHITE);
                
                setVisible(true);
	}
}