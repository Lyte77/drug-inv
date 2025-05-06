from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import F, Sum, ExpressionWrapper, DecimalField,Count
from decimal import Decimal
from django.db import DatabaseError
import logging
from .models import Drug
from orders.models import Order
from django.contrib import messages
from .forms import AddDrugForm
from django.template.loader import render_to_string

import json
from django.http import JsonResponse

from django.http import HttpResponse


# Create your views here.
logger = logging.getLogger(__name__)
def dashboard_view(request):
  try:
        total_drugs = Drug.objects.all().count()
        total_orders = Order.objects.all().count()
        metrics = database_computations()
        total_profit = get_total_profit()
        drug_form = AddDrugForm()

        
        check_target()
        
        
        context = {
                    'total_drugs':total_drugs, 
                    'total_orders':total_orders,
                    'total_profit':total_profit,
                    'drug_form':drug_form,
                    **metrics
                    
                    }

        return render(request, 'inventory/dashboard.html', context)
  except DatabaseError as e:
      logger.error(f"Database error in dashboard_view:{e}")
      messages.error(request, "Unable to load dashboard.")
      return render(request, 'inventory/error.html', status=500)

def database_computations():
    order_aggregates = Order.objects.aggregate(
        total_payment=Sum('paid_amount'),
        
        debt = Sum(ExpressionWrapper(
            F('price') * F('quantity') - F('paid_amount'),
            output_field=DecimalField()
        ))
      
    )
    drug_aggregates = Drug.objects.aggregate(
        company_payment=Sum(ExpressionWrapper(
            F('price') * F('quantity'),
            output_field=DecimalField()
        )),
    )
    return{
      'total_payment': order_aggregates['total_payment'] or Decimal('0.00'),
      'total_debt': order_aggregates['debt'] or Decimal('0.00'),
      'company_total': drug_aggregates['company_payment'] or Decimal('0.00')

    }
def get_total_profit():
    total_profit = Order.objects.annotate(
        profit=ExpressionWrapper(
            (F('price') - F('company_price')) * F('quantity'),
            output_field=DecimalField()
        )
    ).aggregate(total=Sum('profit'))['total']

    return total_profit or 0 

def check_target():
   order_aggregates = Order.objects.aggregate(
        total_payment=Sum('paid_amount'),
        
        debt = Sum(ExpressionWrapper(
            F('price') * F('quantity') - F('paid_amount'),
            output_field=DecimalField()
        ))
      
    )
   drug_aggregates = Drug.objects.aggregate(
        company_payment=Sum(ExpressionWrapper(
            F('price') * F('quantity'),
            output_field=DecimalField()
        )),
    )
   
   if order_aggregates['total_payment'] != drug_aggregates['company_payment']:
        print(f"Opps not yet target")
   elif order_aggregates['total_payment'] ==  drug_aggregates['company_payment']:
       print("Youve reach your target")
   else:
       pass



def drugs_view(request):
    drugs = Drug.objects.all()
    drug_form = AddDrugForm()
    context = {'drugs': drugs,
               'drug_form':drug_form}
    return render(request, 'inventory/drugs_page.html' ,context)



def chart(request):
    pass



def add_drug(request):
    if request.method == 'POST':
        drug_form = AddDrugForm(request.POST)
        if drug_form.is_valid():
            new_drug = drug_form.save()

            # Prepare the new table row
            context = {'drug': new_drug}
            messages.success(request, "Drug added succesfully")
            response = render(request, 'partials/table/drug_row.html', context)
            return response
            # Prepare the HX-Trigger with toast message
            
        else:
            return HttpResponse(status=400)






def edit_drug(request, pk):
    drug = get_object_or_404(Drug, pk=pk)

    if request.method == 'POST':
        form = AddDrugForm(request.POST, instance=drug)
        if form.is_valid():
            updated_drug = form.save()
            messages.success(request, "Drug updated succesfully")
            return render(request, 'partials/table/drug_row.html', {'drug': updated_drug})
    else:
        form = AddDrugForm(instance=drug)
    
    response = render(request, 'partials/forms/edit_drug_modal.html', {'form':form, 'drug':drug})
    response['HX-Trigger'] = 'success'
    return response                                                        


def delete_drug(request,pk):
     drug = get_object_or_404(Drug, pk=pk)
     if request.method == "DELETE":
        drug.delete()
        messages.success(request,'Drug removed')
        return render(request,'partials/toast/toast.html' )
     return HttpResponse(status=405)
         
     


    


