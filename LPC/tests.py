from django.test import TestCase

# Create your tests here.

if __name__ == '__main__':
        # instance-0000322e-3f6c30d6-e029-49c6-ab20-aa502fdbe557-tape7c7968e-bf
        str='instance-0000322e-3f6c30d6-e029-49c6-ab20-aa502fdbe557-tape7c7968e-bf'
        tmp=str.find('-tap')
        print(str.__contains__('instance'))
        print(str[18:54])