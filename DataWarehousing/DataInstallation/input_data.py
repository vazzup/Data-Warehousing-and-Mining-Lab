#!/usr/bin/env python3

import csv, MySQLdb as mdb

def create_tables(curs):
    curs.execute('DROP TABLE IF EXISTS revenue')
    curs.execute('DROP TABLE IF EXISTS customers')
    curs.execute('DROP TABLE IF EXISTS plans')
    curs.execute('DROP TABLE IF EXISTS regions')
    sql1 = 'CREATE  TABLE IF NOT EXISTS customers(phone_no varchar(20) PRIMARY KEY,\
                                            name varchar(40),\
                                            call_usg int,\
                                            data_usg int,\
                                            sms_usg int);'
    sql2 = 'CREATE TABLE IF NOT EXISTS plans(code int PRIMARY KEY,\
                                            call_all int,\
                                            data_all int,\
                                            sms_all int,\
                                            cost_m int);'
    sql3 = 'CREATE TABLE IF NOT EXISTS regions(code int PRIMARY KEY,\
                                                type varchar(20),\
                                                name varchar(40));'
    sql4 = 'CREATE TABLE IF NOT EXISTS revenue(region_code int NOT NULL,\
                                                plan_code int NOT NULL,\
                                                phone_no varchar(20) NOT NULL,\
                                                revenue_m int,\
                                                revenue_over int,\
                                                call_un int,\
                                                data_un int,\
                                                sms_un int,\
                                                FOREIGN KEY(region_code) references regions(code),\
                                                FOREIGN KEY(plan_code) references plans(code),\
                                                FOREIGN KEY(phone_no) references customers(phone_no));'
    try:
        curs.execute(sql1)
    except:
        print('Error in sql1')
        pass
    try:
        curs.execute(sql2)
    except:
        print('Error in sql2')
        pass
    try:
        curs.execute(sql3)
    except:
        print('Error in sql3')
        pass
    try:
        curs.execute(sql4)
    except:
        print('Error in sql4')
        pass
    return

def insert_customers(conn, curs):
    sql = 'INSERT INTO customers VALUES(\'{0}\', \'{1}\', {2}, {3}, {4});'
    csv_data = csv.reader(open('Customer.csv'))
    first_row = True
    for row in csv_data:
        for i in range(len(row)):
            if row[i] is ' ' or row[i] is '':
                row[i] = 'NULL'
        if first_row:
            first_row = False
            continue
        curs.execute(sql.format(*row))
    conn.commit()
    return

def insert_regions(conn, curs):
    sql = 'INSERT INTO regions VALUES({0}, \'{1}\', \'{2}\');'
    csv_data = csv.reader(open('region.csv'))
    first_row = True
    for row in csv_data:
        for i in range(len(row)):
            if row[i] is ' ' or row[i] is '':
                row[i] = 'NULL'
        if first_row:
            first_row = False
            continue
        curs.execute(sql.format(*row))
    conn.commit()
    return

def insert_plans(conn, curs):
    sql = 'INSERT INTO plans VALUES({0}, {1}, {2}, {3}, {4});'
    csv_data = csv.reader(open('plans.csv'))
    first_row = True
    for row in csv_data:
        for i in range(len(row)):
            if row[i] is ' ' or row[i] is '':
                row[i] = 'NULL'
        if first_row:
            first_row = False
            continue
        curs.execute(sql.format(*row))
    conn.commit()
    return

def insert_plans(conn, curs):
    sql = 'INSERT INTO plans VALUES({0}, {1}, {2}, {3}, {4});'
    csv_data = csv.reader(open('plans.xlsx'))
    first_row = True
    for row in csv_data:
        for i in range(len(row)):
            if row[i] is ' ' or row[i] is '':
                row[i] = 'NULL'
        if first_row:
            first_row = False
            continue
        curs.execute(sql.format(*row))
    conn.commit()
    return

def insert_revenue(conn, curs):
    sql = 'INSERT INTO revenue VALUES({0}, {1}, \'{2}\', {3}, {4}, {5}, {6}, {7});'
    csv_data = csv.reader(open('revenue.csv'))
    first_row = True
    for row in csv_data:
        for i in range(len(row)):
            if row[i] is ' ' or row[i] is '':
                row[i] = '0'
        if first_row:
            first_row = False
            continue
        curs.execute(sql.format(*row))
    conn.commit()
    return

def cleanup(conn, curs):
    sql = 'DELETE FROM customers WHERE\
            (call_usg IS NULL) OR\
            (data_usg IS NULL) OR\
            (sms_usg IS NULL);'
    curs.execute(sql)
    conn.commit()
    return

def update_revenue(conn, curs):
    sql = 'UPDATE revenue a INNER JOIN plans b ON a.plan_code = b.code SET a.revenue_m = b.cost_m;'
    curs.execute(sql)
    # sql = 'UPDATE revenue a SET a.revenue_over = 0;'
    # curs.execute(sql)
    sql = 'UPDATE revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no SET a.revenue_over = (a.revenue_over + c.call_usg - b.call_all)*0.01 WHERE (a.phone_no = c.phone_no) AND (c.call_usg > b.call_all);'
    curs.execute(sql)
    sql = 'UPDATE revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no SET a.revenue_over = (a.revenue_over + c.data_usg - b.data_all)*0.05 WHERE (a.phone_no = c.phone_no) AND (c.data_usg > b.data_all);'
    curs.execute(sql)
    sql = 'UPDATE revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no SET a.revenue_over = (a.revenue_over + c.sms_usg - b.sms_all)*0.05 WHERE (a.phone_no = c.phone_no) AND (c.sms_usg > b.sms_all);'
    curs.execute(sql)
    sql = 'UPDATE revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no SET a.call_un = (b.call_all - c.call_usg) WHERE (a.phone_no = c.phone_no) AND (c.call_usg < b.call_all);'
    curs.execute(sql)
    sql = 'UPDATE revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no SET a.data_un = b.data_all - c.data_usg WHERE (a.phone_no = c.phone_no) AND (c.data_usg < b.data_all);'
    curs.execute(sql)
    sql = 'UPDATE revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no SET a.sms_un = b.sms_all - c.sms_usg WHERE (a.phone_no = c.phone_no) AND (c.sms_usg < b.sms_all);'
    curs.execute(sql)
    conn.commit()
    return

def get_slice_query(conn, curs):
    sql = 'SELECT * FROM (revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no INNER JOIN regions d ON a.region_code = d.code) WHERE d.type = \'rural\';'
    curs.execute(sql)
    rows = curs.fetchall()
    print('The rural users are...')
    max_len = [0] * len(rows[0])

    rows = list(rows)

    for i in range(len(rows)):
        rows[i] = list(map(str, list(rows[i])))

    for row in rows:
        i = 0
        for datum in row:
            max_len[i] = max(max_len[i], len(datum))
            i += 1

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if len(str(rows[i][j])) < max_len[j]:
                rows[i][j] = rows[i][j] + (" " * (max_len[j] - len(rows[i][j])))

    for row in rows:
        for item in row:
            print(item, end = ' ')
        print()
    sql = 'SELECT sum(a.revenue_m), sum(a.revenue_over) FROM (revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no INNER JOIN regions d ON a.region_code = d.code) WHERE d.type = \'rural\';'
    curs.execute(sql)
    row = curs.fetchone()
    print('The total monthly revenue is {0} and the revenue due to overuse is {1} from rural areas'.format(row[0], row[1]))
    return

def get_dice_query(conn, curs):
    sql = 'SELECT * FROM (revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no INNER JOIN regions d ON a.region_code = d.code) WHERE d.type = \'urban\' AND a.revenue_m > 200;'
    curs.execute(sql)
    rows = curs.fetchall()
    print('The urban users with monthly revenue greater than 200 are...')
    max_len = [0] * len(rows[0])

    rows = list(rows)

    for i in range(len(rows)):
        rows[i] = list(map(str, list(rows[i])))

    for row in rows:
        i = 0
        for datum in row:
            max_len[i] = max(max_len[i], len(datum))
            i += 1

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if len(str(rows[i][j])) < max_len[j]:
                rows[i][j] = rows[i][j] + (" " * (max_len[j] - len(rows[i][j])))

    for row in rows:
        for item in row:
            print(item, end = ' ')
        print()
    sql = 'SELECT sum(a.revenue_m), sum(a.revenue_over) FROM (revenue a INNER JOIN plans b ON a.plan_code = b.code INNER JOIN customers c ON a.phone_no = c.phone_no INNER JOIN regions d ON a.region_code = d.code) WHERE d.type = \'urban\' AND a.revenue_m > 200;'
    curs.execute(sql)
    row = curs.fetchone()
    print('The total monthly revenue is {0} and the revenue due to overuse is {1} from rural areas'.format(row[0], row[1]))
    return

def main():
    hostname, username, password, database = 'localhost', 'root', 'dwmissucks'\
                                                                        , 'DWM'
    conn = mdb.connect(host = hostname,
                        user=username,
                        passwd=password,
                        db=database)
    curs = conn.cursor()
    print('Creating tables...')
    create_tables(curs)
    print('Read from and insert data into customers...')
    insert_customers(conn, curs)
    print('Read from and insert data into regions...')
    insert_regions(conn, curs)
    print('Read from and insert data into plans...')
    insert_plans(conn, curs)
    print('Cleanup NULL values in all three tables...')
    cleanup(conn, curs)
    print('Insert data into revenue table...')
    insert_revenue(conn, curs)
    print('Calculate NULL column values and update in revenue table...')
    update_revenue(conn, curs)
    print('Execute slice... Find details of customers from rural areas...')
    get_slice_query(conn, curs)
    print('Execute dice... Find details of customers from urban areas with monthly revenue more than 200...')
    get_dice_query(conn, curs)
    return

if __name__ == '__main__':
    main()
