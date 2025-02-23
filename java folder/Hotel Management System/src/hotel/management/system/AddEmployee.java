package hotel.management.system;


import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class AddEmployee extends JFrame{ //Third Frame

    
	JTextField NameeField,AgeField,SalaryField,PhoneField,AAdharrField,EmailField;
    JRadioButton Male,Female;
    JButton SaveButton;
    JComboBox JobbCombo;

        public AddEmployee(){
            getContentPane().setForeground(Color.BLUE);
            getContentPane().setBackground(Color.WHITE);
            setTitle("ADD EMPLOYEE DETAILS");
		 
            setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
            setSize(778,486);
            getContentPane().setLayout(null);
			
            JLabel Namee = new JLabel("NAME");
            Namee.setFont(new Font("Tahoma", Font.PLAIN, 17));
            Namee.setBounds(60, 30, 150, 27);
            add(Namee);
            
            NameeField = new JTextField();
            NameeField.setBounds(160, 30, 200, 27);
            NameeField.setFont(new Font("Tahoma", Font.PLAIN, 16));
            add(NameeField);		
			
            JLabel Age = new JLabel("AGE");
            Age.setFont(new Font("Tahoma", Font.PLAIN, 17));
            Age.setBounds(60, 80, 150, 27);
            add(Age);
			
            AgeField = new JTextField();
            AgeField.setFont(new Font("Tahoma", Font.PLAIN, 16));            
            AgeField.setBounds(160, 80, 200, 27);
            add(AgeField);
            
            JLabel Gender = new JLabel("GENDER");
            Gender.setFont(new Font("Tahoma", Font.PLAIN, 17));
            Gender.setBounds(60, 120, 150, 27);
            add(Gender);
		
            Male = new JRadioButton("MALE",true);
            Male.setBackground(Color.WHITE);
            Male.setFont(new Font("Tahoma", Font.PLAIN, 16)); 
            Male.setBounds(160, 120, 95, 27);
            add(Male);
	
            Female = new JRadioButton("FEMALE");
            Female.setFont(new Font("Tahoma", Font.PLAIN, 16)); 
            Female.setBackground(Color.WHITE);
            Female.setBounds(260, 120, 100, 27);
            add(Female);

            ButtonGroup bg = new ButtonGroup();
            bg.add(Male);
            bg.add(Female);

   
            
            JLabel Jobb = new JLabel("JOB");
            Jobb.setFont(new Font("Tahoma", Font.PLAIN, 17));
            Jobb.setBounds(60, 170, 150, 27);
            add(Jobb);
			
            String jobs[] = {"Front Desk Clerks","Porters","Housekeeping","Kitchen Staff","Room Service","Waiter/Waitress","Manager","Accountant","Chef"};
            JobbCombo = new JComboBox(jobs);
            JobbCombo.setBackground(Color.WHITE);
            JobbCombo.setBounds(160,170,200,30);
            JobbCombo.setFont(new Font("Tahoma", Font.PLAIN, 16));
            add(JobbCombo);
            		
            JLabel Salary = new JLabel("SALARY");
            Salary.setFont(new Font("Tahoma", Font.PLAIN, 17));
            Salary.setBounds(60, 220, 150, 27);
            add(Salary);
			
            SalaryField = new JTextField();
            SalaryField.setBounds(160, 220, 200, 27);
            SalaryField.setFont(new Font("Tahoma", Font.PLAIN, 16));
            add(SalaryField);
	
            JLabel Phone = new JLabel("PHONE");
            Phone.setFont(new Font("Tahoma", Font.PLAIN, 17));
            Phone.setBounds(60, 270, 150, 27);
            add(Phone);
	
            PhoneField = new JTextField();
            PhoneField.setBounds(160, 270, 200, 27);
            PhoneField.setFont(new Font("Tahoma", Font.PLAIN, 16));
            add(PhoneField);
	
            JLabel AAdharr = new JLabel("AADHAR");
            AAdharr.setFont(new Font("Tahoma", Font.PLAIN, 17));
            AAdharr.setBounds(60, 320, 150, 27);
            add(AAdharr);
			
            AAdharrField = new JTextField();
            AAdharrField.setBounds(160, 320, 200, 27);
            AAdharrField.setFont(new Font("Tahoma", Font.PLAIN, 16));
            add(AAdharrField);
	
            
            JLabel email = new JLabel("EMAIL");
            email.setFont(new Font("Tahoma", Font.PLAIN, 17));
            email.setBounds(60, 370, 150, 27);
            add(email);
			
            EmailField = new JTextField();
            EmailField.setBounds(160, 370, 200, 27);
            EmailField.setFont(new Font("Tahoma", Font.PLAIN, 16));
            add(EmailField);
	
            setVisible(true);

            SaveButton = new JButton("SAVE");
            SaveButton.setBounds(160, 420, 200, 30);
            SaveButton.setBackground(Color.BLACK);
            SaveButton.setForeground(Color.WHITE);
            add(SaveButton);
            
	
            JLabel AddPassengers = new JLabel("ADD EMPLOYEE DETAILS");
            AddPassengers.setForeground(Color.BLUE);
            AddPassengers.setFont(new Font("Tahoma", Font.PLAIN, 31));
            AddPassengers.setBounds(480, 24, 442, 35);
            add(AddPassengers);		

            ImageIcon i1 = new ImageIcon(ClassLoader.getSystemResource("icons/tenth.jpg"));
            Image i3 = i1.getImage().getScaledInstance(500, 500,Image.SCALE_DEFAULT);
            ImageIcon i2 = new ImageIcon(i3);
            JLabel image = new JLabel(i2);
            image.setBounds(410,80,480,410);
            add(image);

            
            SaveButton.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ae){
                    String name = NameeField.getText();
                    String age = AgeField.getText();
                    String job = (String)JobbCombo.getSelectedItem();
                    String salary = SalaryField.getText();
                    String phone = PhoneField.getText();
                    String aadhar = AAdharrField.getText();
                    String email = EmailField.getText();
                   
                    String gender = null;
                    if(Male.isSelected()){
                        gender = "Male";
                    
                    }else if(Female.isSelected()){
                        gender = "Female";
                    }
                    // if (email.equals("") && email.includes("@") && includes(".com")){JOptionPane.showMessageDialog(null,"Email is Invalid"); return;}
                    if (name.equals("")){JOptionPane.showMessageDialog(null,"Name Should Not Be Empty"); return;}
                    if (age.equals("")){JOptionPane.showMessageDialog(null,"Age Should Not Be Empty");return;}
                    if (job.equals("")){JOptionPane.showMessageDialog(null,"Job Should Not Be Empty");return;}
                    if (salary.equals("")){JOptionPane.showMessageDialog(null,"Salary Should Not Be Empty");return;}
                    if (phone.equals("")){JOptionPane.showMessageDialog(null,"Phone Should Not Be Empty");return;}
                    if (aadhar.equals("")){JOptionPane.showMessageDialog(null,"Aadhar Should Not Be Empty");return;}
                    if (email.equals("")){JOptionPane.showMessageDialog(null,"Email Should Not Be Empty");return;}
                    if (gender.equals(null)){JOptionPane.showMessageDialog(null,"Gender Should Not Be Empty");return;}


                    
                    


                            
                    
                    
                    try {
                        conn c = new conn();
   
                        String str = "INSERT INTO employee values( '"+name+"', '"+age+"', '"+gender+"','"+job+"', '"+salary+"', '"+phone+"', '"+email+"','"+aadhar+"')";
                        
                        c.s.executeUpdate(str);
                        JOptionPane.showMessageDialog(null,"Employee Added Successfully");
                        // setVisible(false);
                    
                    } catch (Exception e) {
                        e.printStackTrace();
        	    }
		}
            });
			
            // setSize(900,600);
            // setVisible(true);
            // setLocation(530,200);
            
            getContentPane().setBackground(Color.white);
            setVisible(true);
            setBounds(300,130,950,600);
			
	}
        
    public static void main(String[] args){
        new AddEmployee();
    }   
}