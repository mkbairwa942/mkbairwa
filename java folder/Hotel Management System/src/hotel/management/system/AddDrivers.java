
package hotel.management.system;


import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class AddDrivers extends JFrame implements ActionListener{

    private JPanel contentPane;
    private JTextField Namee_Field,Agee_Field,Car_Company_Field,Car_Brand_Field, Location_Field;
    private JComboBox comboBox, comboBox_1;
    JButton Add_Button,Back_Button;
    Choice c1;

    public static void main(String[] args) {
        new AddDrivers().setVisible(true);
    }


    public AddDrivers() {
    setBounds(280, 200, 1000, 500);
	contentPane = new JPanel();
	setContentPane(contentPane);
	contentPane.setLayout(null);
        
    ImageIcon i1  = new ImageIcon(ClassLoader.getSystemResource("icons/eleven.jpg"));
    Image i3 = i1.getImage().getScaledInstance(500, 300,Image.SCALE_DEFAULT);
    ImageIcon i2 = new ImageIcon(i3);
    JLabel l15 = new JLabel(i2);
    l15.setBounds(400,30,500,370);
    add(l15);
        
    JLabel l10 = new JLabel("Add Drivers");
    l10.setFont(new Font("Tahoma", Font.BOLD, 18));
	l10.setBounds(150, 10, 120, 22);
	contentPane.add(l10);
        
	JLabel Namee = new JLabel("Name");
	Namee.setForeground(new Color(25, 25, 112));
	Namee.setFont(new Font("Tahoma", Font.BOLD, 14));
	Namee.setBounds(64, 70, 102, 22);
	contentPane.add(Namee);
        
    Namee_Field = new JTextField();
	Namee_Field.setBounds(174, 70, 156, 20);
    Namee_Field.setFont(new Font("Tahoma", Font.BOLD, 14));
	contentPane.add(Namee_Field);
        
	JLabel Agee = new JLabel("Age");
	Agee.setForeground(new Color(25, 25, 112));
	Agee.setFont(new Font("Tahoma", Font.BOLD, 14));
	Agee.setBounds(64, 110, 102, 22);
	contentPane.add(Agee);
        
    Agee_Field = new JTextField();
	Agee_Field.setBounds(174, 110, 156, 20);
    Agee_Field.setFont(new Font("Tahoma", Font.BOLD, 14));
	contentPane.add(Agee_Field);

	JLabel Gender = new JLabel("Gender");
	Gender.setForeground(new Color(25, 25, 112));
	Gender.setFont(new Font("Tahoma", Font.BOLD, 14));
	Gender.setBounds(64, 150, 102, 22);
	contentPane.add(Gender);
        
    comboBox = new JComboBox(new String[] { "Male", "Female" });
	comboBox.setBounds(176, 150, 154, 20);
	contentPane.add(comboBox);

	JLabel Car_Company = new JLabel("Car Company");
	Car_Company.setForeground(new Color(25, 25, 112));
	Car_Company.setFont(new Font("Tahoma", Font.BOLD, 14));
	Car_Company.setBounds(64, 190, 102, 22);
	contentPane.add(Car_Company);
        
    Car_Company_Field = new JTextField();
	Car_Company_Field.setBounds(174, 190, 156, 20);
    Car_Company_Field.setFont(new Font("Tahoma", Font.BOLD, 14));
	contentPane.add(Car_Company_Field);

    JLabel Car_Brand = new JLabel("Car Brand");
	Car_Brand.setForeground(new Color(25, 25, 112));
	Car_Brand.setFont(new Font("Tahoma", Font.BOLD, 14));
	Car_Brand.setBounds(64, 230, 102, 22);
	contentPane.add(Car_Brand);

    Car_Brand_Field = new JTextField();
	Car_Brand_Field.setBounds(174, 230, 156, 20);
    Car_Brand_Field.setFont(new Font("Tahoma", Font.BOLD, 14));
	contentPane.add(Car_Brand_Field);
	
    JLabel Available = new JLabel("Available");
	Available.setForeground(new Color(25, 25, 112));
	Available.setFont(new Font("Tahoma", Font.BOLD, 14));
	Available.setBounds(64, 270, 102, 22);
	contentPane.add(Available);

    comboBox_1 = new JComboBox(new String[] { "Yes", "No" });
	comboBox_1.setBounds(176, 270, 154, 20);
	contentPane.add(comboBox_1);

    JLabel Location = new JLabel("Location");
	Location.setForeground(new Color(25, 25, 112));
	Location.setFont(new Font("Tahoma", Font.BOLD, 14));
	Location.setBounds(64, 310, 102, 22);
	contentPane.add(Location);

    Location_Field = new JTextField();
	Location_Field.setBounds(174, 310, 156, 20);
    Location_Field.setFont(new Font("Tahoma", Font.BOLD, 14));
	contentPane.add(Location_Field);

	Add_Button = new JButton("Add");
	Add_Button.addActionListener(this);
	Add_Button.setBounds(64, 380, 111, 33);
    Add_Button.setBackground(Color.BLACK);
    Add_Button.setForeground(Color.WHITE);
	contentPane.add(Add_Button);

	Back_Button = new JButton("Back");
	Back_Button.addActionListener(this);
	Back_Button.setBounds(198, 380, 111, 33);
    Back_Button.setBackground(Color.BLACK);
    Back_Button.setForeground(Color.WHITE);
	contentPane.add(Back_Button);

	
    contentPane.setBackground(Color.WHITE);
    
    }
    
    public void actionPerformed(ActionEvent ae){
        try{
            
            if(ae.getSource() == Add_Button){
                try{
                conn c = new conn();
                String name = Namee_Field.getText();
                String age = Agee_Field.getText();
                String gender = (String)comboBox.getSelectedItem();
                String company  = Car_Company_Field.getText();
                String brand = Car_Brand_Field.getText();
                String available = (String)comboBox_1.getSelectedItem();
                String location = Location_Field.getText();
                String str = "INSERT INTO driver values( '"+name+"', '"+age+"', '"+gender+"','"+company+"', '"+brand+"', '"+available+"','"+location+"')";
                System.out.println("Sql Query is :"+str);
                if (name.equals("")){JOptionPane.showMessageDialog(null,"Name Should Not Be Empty"); return;}
                if (age.equals("")){JOptionPane.showMessageDialog(null,"Age Should Not Be Empty"); return;}
                if (company.equals("")){JOptionPane.showMessageDialog(null,"Company Should Not Be Empty"); return;}
                if (brand.equals("")){JOptionPane.showMessageDialog(null,"Brand Should Not Be Empty"); return;}
                if (location.equals("")){JOptionPane.showMessageDialog(null,"Location Should Not Be Empty"); return;}
                
		c.s.executeUpdate(str);
		JOptionPane.showMessageDialog(null, "Driver Successfully Added");
                this.setVisible(false);
               
                }catch(Exception ee){
                    System.out.println(ee);
                }
            }
            else if(ae.getSource() == Back_Button){
                this.setVisible(false);
            }
        }catch(Exception eee){
            
        }
    }
}