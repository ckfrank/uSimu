from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from rango.models import Category
from rango.models import Page
from rango.models import Submission
from rango.models import Feedback
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from rango.forms import SubmissionForm
from django.core.paginator import Paginator
from rango.models import CPU_Family, CPU

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    user = request.user
    submissions = Submission.objects.filter(owner_id=user.id).order_by('-id')[:10]
    feedbacks = Feedback.objects.filter(referring_submission__owner_id=user.id).order_by('-id')[:10]
    total_submissions = Submission.objects.filter(owner_id=user.id)
    success_count = total_submissions.filter(result="Success").count()
    pending_count = total_submissions.filter(result="Pending").count()
    fail_count = total_submissions.filter(result="Fail").count()
    warning_count = total_submissions.filter(result="Warning").count()
    # print(submissions)

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['submissions'] = submissions
    context_dict['feedbacks'] = feedbacks
    context_dict['success_count'] = success_count
    context_dict['pending_count'] = pending_count
    context_dict['fail_count'] = fail_count
    context_dict['warning_count'] = warning_count

    visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']
    # Obtain response from coockie info
    response = render(request, 'rango/index.html', context=context_dict)
    # Call helper function to handle coockie

    # Return a rendered response to send to the client
    return response
    # # this is the test cookie
    # request.session.set_test_cookie()
    # return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # Context dict is not needed here!
    # print(request.method)
    # print(request.user)
    # # reciving test cookie
    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()
    # need context dic for counting visits
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/contact.html', context=context_dict)
    return response


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # try to finde category name slug with given name
        category = Category.objects.get(slug=category_name_slug)
        # retrieve all associated pages, filter them
        pages = Page.objects.filter(category=category)

        # add results list to template context under key pages
        context_dict['pages'] = pages
        # also for category
        context_dict['category'] = category
    except Category.DoesNotExist:
        # did not find the specified category
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    # HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # cannot add a page to a Cat that is not exist
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


# Decommissioned
# def register(request):
#     # goes to page 157 for detail
#     # bool value for successful registration
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#             profile.save()
#             registered = True
#
#         else:
#             print(user_form.errors, profile_form.errors)
#
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# Decommissioned
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('rango:index'))
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


# Decommissioned
# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('rango:index'))


#  server cookie helper
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# Update this fn
def visitor_cookie_handler(request):
    # use 1 instead if the cookie is not exist - new user
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # more than a day from last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update last visit
        request.session['last_visit'] = str(datetime.now())
    else:
        # set last visit cookie
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


@user_passes_test(lambda u: u.is_active and u.is_superuser)
def usimuAdmin(request):
    domain = request.META['HTTP_HOST']
    context_dict = {}
    context_dict['domain'] = domain
    return render(request, 'rango/usimu_admin.html', context=context_dict)


@login_required
def submission(request):
    context_dict = {}
    user = request.user
    submissions = Submission.objects.filter(owner_id=user.id).order_by('-id')

    context_dict['current_user'] = user

    # paginator
    paginator = Paginator(submissions, 5) # every 5 items a page
    page_num = request.GET.get('page', default=1) # invalid number set to 1
    curr_page_content = paginator.get_page(page_num) # container for current page


    page_list = [x for x in range(curr_page_content.number - 2, curr_page_content.number + 3) if x in paginator.page_range]
    # print(page_list)
    # adding "..."
    if page_list[0] - 1 >= 2:
        page_list.insert(0, "...")
    if paginator.num_pages - page_list[-1]  >= 2:
        page_list.append("...")
    # print(page_list)
    # adding first/last page
    if page_list[0] == "...":
        page_list.insert(0, 1)# first page
    if page_list[-1] != paginator.num_pages:
        page_list.append(paginator.num_pages)# very last page
    print(page_list)

    context_dict['submissions'] = curr_page_content
    context_dict['page_list'] = page_list

    return render(request, 'rango/submissions.html', context=context_dict)


@login_required
def upload_code(request):
    context_dict = {}
    submission_form = None

    try:
        # getting user/their submission/their feedback
        user = request.user
        # add the result
        context_dict['current_user'] = user
        # to POST a submission
        cpu_url = reverse_lazy("rango:ajax_load_cpus")
        new_submission = None
        submission_form = SubmissionForm()
        if request.method == 'POST':
            submission_form = SubmissionForm(request.POST)
            # print(request.POST)

            if submission_form.is_valid():
                # do not commit yet, something to add
                new_submission = submission_form.save(commit=False)
                # assign current owner
                new_submission.owner = request.user
                cpu = CPU.objects.get(id=int(request.POST.get("cpu")))
                new_submission.cpu = cpu
                # print(request)
                new_submission.save()
                messages.success(request, "Successfully Submitted!")
                return redirect('rango:submissions')

            else:
                print(submission_form.errors)
                new_submission = SubmissionForm()

        context_dict['new_submission'] = new_submission



    except Submission.DoesNotExist:
        # specified submission not found
        context_dict['submissions'] = None

    context_dict['submission_form'] = submission_form
    context_dict['cpu_url'] = cpu_url
    return render(request, 'rango/upload_code.html', context=context_dict)

@login_required
def submission_detail(request, submission_id):
    context_dict ={}
    submission = Submission.objects.get(id=int(submission_id))
    title = str(submission.title)

    context_dict['title'] = title
    return render(request, 'rango/submission_detail.html', context=context_dict)

def load_cpu(request):
    context_dict = {}
    family_id = request.GET.get('cpu_family')
    family = CPU_Family.objects.get(pk=family_id)
    cpus = CPU.objects.filter(family=family).order_by('name')
    context_dict['cpus'] = cpus
    return render(request, template_name='rango/load_cpus.html',context=context_dict)