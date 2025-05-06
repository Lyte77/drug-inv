from django.shortcuts import render,get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import AddOrderform
from django.contrib import messages
from .models import Order

# Create your views here.

def all_orders(request):
     form = AddOrderform()
     orders = Order.objects.all()
     context = {'orders':orders,
                'form':form}
     return render(request, 'orders/all_orders.html',context)

def add_order(request):
    orders = Order.objects.all()
    if request.method == 'POST':
        form = AddOrderform(request.POST)
        if form.is_valid(): 
            order = form.save()
            messages.success(request, "Order created succesfully")
            total_orders = Order.objects.all().count()
            total_debt = sum(order.balance_due() for order in orders )
            total_payment = sum(order.get_total_price() for order in orders )
            total_company_payment =  sum(order.get_company_price() for order in orders)
            # total_profit_made = sum(order.profit() for order in orders) 
            total_profit_made = total_payment - total_company_payment
            print(f"Total Profit:{total_profit_made}")



        # rendering partials
        order_row_html = render_to_string('partials/table/order_row.html', {'order': order})
        total_orders_html = render_to_string('partials/cards/order_card.html', {'total_orders': total_orders})
        total_dept_html = render_to_string('partials/cards/total_debts_card.html', {'total_debt': total_debt})
        total_payment_html = render_to_string('partials/cards/total_payment_card.html', {'total_payment': total_payment})
        total_company_html = render_to_string('partials/cards/total_company_price_card.html', {'total_company_payment': total_company_payment})
        total_profit_html = render_to_string('partials/cards/total_profit_made_card.html', {'total_profit_made': total_profit_made})


        return HttpResponse(order_row_html + total_orders_html + total_dept_html +str(total_payment_html) + str(total_company_html) + total_profit_html)

    else:
            # On validation errors
        return render(request, 'includes/create_order.html', {'form': form}, status=400)
    

def edit_order(request, pk):
        order = get_object_or_404(Order, pk=pk)

        if request.method == 'POST':
            form = AddOrderform(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, "Order updated succesfully")
                return render(request,'partials/table/order_row.html',{ 'order':order})

        else:
            form = AddOrderform(instance=order)
        
        response = render(request, 'partials/modals/edit_orders_modal.html', {'form':form, 'order':order})
        response['HX-Trigger'] = 'success'
        return response


def delete_order(request,pk):
     order = get_object_or_404(Order,pk=pk)
     if request.method == 'DELETE':
        order.delete()
        messages.success(request, 'Order removed')
        return render(request,'partials/toast/toast.html' )
     return HttpResponse(status=405)
          

