import MySQLdb
import sys
import time
import os
import subprocess
import cmd
############# Removing database warnings #############
from warnings import filterwarnings
import MySQLdb as Database
filterwarnings('ignore', category = Database.Warning)


class Database(cmd.Cmd):
    __host = '127.0.0.1'
    __user = 'root'
    __password = ''
    __port = 3306
    __database = 'pythontest'
    

    def get_dictionary(self, table='orders'):
        print "in get dictionary"
        import MySQLdb.cursors
        conn = MySQLdb.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__password, db=self.__database, cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * from {}".format(table))
        return cursor.fetchall()

    def do_dictionary_to_yaml(self, line):
        """Invokes get_dictionary for orders table
            then converts to yaml
        """
        import yaml
        data = self.get_dictionary()    
        orders_list = []
        
    #   Converting values with L(long) from db to int
        for dic in data:
          d = {}
          for k,v in dic.items():                
            d[k] = int(dic[k]) if type(dic[k]) == long else dic[k]
          orders_list.append(d)

    #   Writing output to result.yaml file
        directory = './out'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory,'orders.yml'), 'w') as yaml_file:
          yaml_file.write( yaml.dump(orders_list, default_flow_style=False))

    def do_build(self, line):
        pass

    def do_release(self, line):
        pass

    def do_deploy(self, line):
        import git

        repo_dir = os.path.join(os.path.dirname(__file__), './')
        repo = git.Repo.init(repo_dir)
        print repo
        repo = git.Repo(repo_dir)
        print repo.git.status()
        # add all files
        print "here"
        print repo.git.add('*')
        # commit
        
        print repo.git.commit(message='Database Dump 2' )
        # now we are one commit ahead
        print repo.git.status()
        #finally pushing the code
        repo.git.push(repo.head)

        #here is the new change
        repo.git.push()

    def do_EOF(self, line):
        return True

    

def main():
    d = Database()
    #d.do_get_dictionary()
    d.do_dictionary_to_yaml()

if __name__ == '__main__':
    #main()
    Database().cmdloop()




