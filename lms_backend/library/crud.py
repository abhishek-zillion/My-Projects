'''
1)
student1=User.objects.get(username='student1')
book_reqs_by_stu1=BookRequest.objects.filter(user=student1)
reverse_book_reqs_by_stu1=student1.bookrequest_set.all()            


2)
book_reqs_by_stu1=BookRequest.objects.filter(user__username='student1')

3)
BookRequest.objects.filter(user__username='student1')[0]
BookRequest.objects.filter(user__username='student1').first()

4)
reqs_on_history=BookRequest.objects.filter(book__title='Sanskrit')

5)
reqs_count_upon_sanskrit=BookRequest.objects.filter(book__title='Sanskrit').count()

6)
reqs_count_on_sanskrit_by_stu1=BookRequest.objects.filter(book__title='Sanskrit', user__username='student1').count()

7)
reqs_count_on_sanskrit_exclude_stu1=BookRequest.objects.filter(book__title='Sanskrit').exclude(user__username='student1').count()

8)
obj.bookrequest_set.all()
reqs=obj.bookrequest_set.all()
    for req in reqs:
        print(req.user,'\n')
'''