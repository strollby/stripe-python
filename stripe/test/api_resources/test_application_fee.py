import stripe
from stripe.test.helper import StripeResourceTest


class ApplicationFeeTest(StripeResourceTest):

    def test_list_application_fees(self):
        stripe.ApplicationFee.list()
        self.requestor_mock.request.assert_called_with(
            'get',
            '/v1/application_fees',
            {}
        )


class ApplicationFeeRefundTest(StripeResourceTest):

    def test_fetch_refund(self):
        fee = stripe.ApplicationFee.construct_from({
            'id': 'fee_get_refund',
            'refunds': {
                'object': 'list',
                'url': '/v1/application_fees/fee_get_refund/refunds',
            }
        }, 'api_key')

        fee.refunds.retrieve("ref_get")

        self.requestor_mock.request.assert_called_with(
            'get',
            '/v1/application_fees/fee_get_refund/refunds/ref_get',
            {},
            None
        )

    def test_list_refunds(self):
        fee = stripe.ApplicationFee.construct_from({
            'id': 'fee_get_refund',
            'refunds': {
                'object': 'list',
                'url': '/v1/application_fees/fee_get_refund/refunds',
            }
        }, 'api_key')

        fee.refunds.list()

        self.requestor_mock.request.assert_called_with(
            'get',
            '/v1/application_fees/fee_get_refund/refunds',
            {},
            None
        )

    def test_update_refund(self):
        def side_effect(*args):
            raise stripe.InvalidRequestError('invalid', 'foo')

        self.requestor_mock.request.side_effect = side_effect

        refund = stripe.ApplicationFeeRefund.construct_from({
            'id': "ref_update",
            'fee': "fee_update",
            'metadata': {},
        }, 'api_key')

        refund.metadata["key"] = "foo"

        try:
            refund.save()
        except stripe.InvalidRequestError:
            pass

        self.requestor_mock.request.assert_called_with(
            'post',
            '/v1/application_fees/fee_update/refunds/ref_update',
            {
                'metadata': {
                    'key': 'foo',
                }
            },
            None
        )

        self.requestor_mock.request.side_effect = None

        refund.metadata["key"] = "bar"
        refund.save()

        self.requestor_mock.request.assert_called_with(
            'post',
            '/v1/application_fees/fee_update/refunds/ref_update',
            {
                'metadata': {
                    'key': 'bar',
                }
            },
            None
        )

    def test_modify_refund(self):
        stripe.ApplicationFeeRefund.modify("fee_update", "ref_update",
                                           metadata={'key': 'foo'},
                                           api_key='api_key')
        self.requestor_mock.request.assert_called_with(
            'post',
            '/v1/application_fees/fee_update/refunds/ref_update',
            {
                'metadata': {
                    'key': 'foo',
                }
            },
            None
        )


class ApplicationFeeRefundsTests(StripeResourceTest):
    def test_create_refund(self):
        stripe.ApplicationFee.create_refund(
            'fee_123'
        )
        self.requestor_mock.request.assert_called_with(
            'post',
            '/v1/application_fees/fee_123/refunds',
            {},
            None
        )

    def test_retrieve_refund(self):
        stripe.ApplicationFee.retrieve_refund(
            'fee_123',
            'fr_123'
        )
        self.requestor_mock.request.assert_called_with(
            'get',
            '/v1/application_fees/fee_123/refunds/fr_123',
            {},
            None
        )

    def test_modify_refund(self):
        stripe.ApplicationFee.modify_refund(
            'fee_123',
            'fr_123',
            metadata={'foo': 'bar'}
        )
        self.requestor_mock.request.assert_called_with(
            'post',
            '/v1/application_fees/fee_123/refunds/fr_123',
            {'metadata': {'foo': 'bar'}},
            None
        )

    def test_list_refunds(self):
        stripe.ApplicationFee.list_refunds(
            'fee_123'
        )
        self.requestor_mock.request.assert_called_with(
            'get',
            '/v1/application_fees/fee_123/refunds',
            {},
            None
        )