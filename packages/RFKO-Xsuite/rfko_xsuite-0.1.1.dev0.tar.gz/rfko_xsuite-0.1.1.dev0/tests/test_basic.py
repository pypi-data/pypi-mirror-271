import RFKO_Xsuite as rfko_xsuite

rfko = rfko_xsuite.Rfko()
rfko.setup_line()
rfko_xsuite.tracking(rfko)

#
# import pkg_resources
# for d in pkg_resources.working_set:
#     if d.key in ['xsuite','xpar','xtrack','xobjects','cpymad']:
#         print(f'{d.key} version: {d.version}')