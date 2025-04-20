from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Image, Category
from django.contrib import messages

@login_required
def image_list(request):
    # Get sort parameter from URL, default to '-upload_date'
    sort = request.GET.get('sort', '-upload_date')
    
    # Validate sort parameter
    valid_sort_fields = ['-upload_date', 'upload_date', '-title', 'title']
    if sort not in valid_sort_fields:
        sort = '-upload_date'
    
    images = Image.objects.all().order_by(sort)
    categories = Category.objects.all()
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(images, 6)  # Show 6 images per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'images/image_list.html', {
        'images': page_obj,
        'categories': categories,
        'page_obj': page_obj,
        'current_sort': sort
    })

@login_required
def image_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image_file = request.FILES.get('image')

        if title and image_file:
            category = None
            if category_id:
                category = get_object_or_404(Category, id=category_id)

            Image.objects.create(
                title=title,
                description=description,
                category=category,
                image=image_file
            )
            messages.success(request, 'Image uploaded successfully!')
            return redirect('images:image_list')
        else:
            messages.error(request, 'Please provide a title and image.')

    categories = Category.objects.all()
    return render(request, 'images/image_upload.html', {'categories': categories})

def custom_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')

@login_required
def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    
    # Get related images from the same category
    if image.category:
        related_images = Image.objects.filter(category=image.category).exclude(id=image.id)[:8]
    else:
        related_images = Image.objects.filter(category__isnull=True).exclude(id=image.id)[:8]
    
    return render(request, 'images/image_detail.html', {
        'image': image,
        'related_images': related_images
    })

@login_required
def category_detail(request, category_id):
    # Get sort parameter from URL, default to '-upload_date'
    sort = request.GET.get('sort', '-upload_date')
    
    # Validate sort parameter
    valid_sort_fields = ['-upload_date', 'upload_date', '-title', 'title']
    if sort not in valid_sort_fields:
        sort = '-upload_date'
    
    if category_id == 'uncategorized':
        images = Image.objects.filter(category__isnull=True).order_by(sort)
        context = {
            'category': {'name': 'Uncategorized Images', 'description': 'Images without a category'},
            'images': images,
            'is_uncategorized': True,
            'current_sort': sort
        }
    else:
        category = get_object_or_404(Category, id=category_id)
        images = category.images.all().order_by(sort)
        context = {
            'category': category,
            'images': images,
            'is_uncategorized': False,
            'current_sort': sort
        }
    return render(request, 'images/category_detail.html', context)
