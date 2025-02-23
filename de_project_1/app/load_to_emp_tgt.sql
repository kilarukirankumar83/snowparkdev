merge into employee_tgt using  (
    select distinct * from employee
) employee
on employee_tgt.first_name = employee.first_name
and employee_tgt.last_name = employee.last_name
when matched then
    update
    set employee_tgt.address = employee.address,
    employee_tgt.city = employee.city,
    employee_tgt.email = employee.email,
    employee_tgt.doj = employee.doj
when not matched then
    insert (first_name, last_name, email, address, city, doj)
    values (employee.first_name, employee.last_name, 
    employee.email, employee.address, 
    employee.city, employee.doj);