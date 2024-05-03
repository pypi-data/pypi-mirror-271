'''
# What is Cost Monitoring Construct?

Cost Monitoring Construct is a CDK library that helps monitor costs for AWS cloud infrastructure resources, such as virtual machines, storage, and network traffic. It allows you to set budgets and alerts to ensure that you don't overspend on your cloud resources.

With the Cost Monitoring Construct, you can share the responsibility of cost management between developers and business holders. This is achieved through the creation of meaningful reports that enable the business team to make informed decisions. Additionally, the Construct generates boilerplate code that can be used to apply these decisions in practice, making it easier to stay on top of your budget.

## How to use Cost Monitoring Construct?

To use Cost Monitoring Construct, all you need is to have the AWS CDK installed and set up. Once you have that, you can install the package from the repository of your choice.

For more information on using this Construct in TypeScript checkout the [TypeScript documentation](docs/typescript.md). You can also check the typescript example from [sample folder](https://github.com/DataChefHQ/cost-monitoring-construct/tree/main/sample) on the GitHub repository.

## Why do you need it?

Cloud services can get very expensive, very quickly, especially if you are not careful with your usage. Cost Monitoring Construct helps you to keep an eye on your cloud infrastructure costs so that you can stay within budget. By setting budgets and defining alert strategies, you can take proactive steps to reduce costs before they become a problem.

## How does Cost Monitoring Construct work?

Cost Monitoring Construct uses AWS Tagging practice to track resources related to an specific application, creates proper alert with respect to the defined budget limit and provide overview dashbords. The tool is highly customizable and allows you to customize it to your budgeting strategy based on your specific needs.

Cost Monitoring Construct provides the following features:

* **Cost dashboard:** Displays your current costs and usage, broken down by application's name, region, and etc. Allows you to see how much you are spending on each application and where you might be able to reduce costs.
* **Budgets:** Allows you to set budgets for each applications. It will automatically set up alerts to notify you when your actual costs exceed your budgeted costs. It also continues to track the cost and sending alert if an application continues to cost drastically.
* **Integration:** Integrates with various tools and monitoring services, such as AWS Cost Explorer and Datadog.

> [!WARNING]
> ApplicationCostMonitoring uses AWS Tags to track resources' usages. You must [activate](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html) your chosen tag key (`cm:application` by default) under Cost Allocation Tags. The tag key will appear in the AWS console up to 24 hours after at least one AWS resource has been created with that tag.

## What is it useful for?

Cost Monitoring Construct is useful for anyone who uses AWS and wants to keep their costs under control. It is particularly useful for:

* **Startups and small businesses:** Cost Monitoring Construct can help startups and small businesses to keep their costs under control during the early stages of growth.
* **Large enterprises:** Cost Monitoring Construct can help large enterprises to optimize their cloud usage and reduce costs across multiple teams and departments.
* **Developers:** Cost Monitoring Construct can help developers to track their usage and costs across multiple projects and services.

## What is this *not* useful for?

The Cost Monitoring Construct is not a magical tool that can solve all of your cloud cost problems. In spite of the fact that it can bring clarity and help you to identify areas where you can reduce costs, you must make the necessary decisions about your infrastructure on your own.

## Which programming languages Cost Monitoring Construct supports?

Cost Monitoring Construct has been developed using JSII technolgy to provide interfaces for different modern programming languages. Currently, it supports the following languages:

* [TypeScript](https://www.npmjs.com/package/cost-monitoring-construct)
* [JavaScript](https://www.npmjs.com/package/cost-monitoring-construct)
* [Python](https://pypi.org/project/cost-monitoring-construct/)
* [.NET](https://www.nuget.org/packages/DataChef.CostMonitoringConstruct)
* [Java](https://central.sonatype.com/artifact/co.datachef/costmonitoringconstruct/1.1.0/versions)

> [!NOTE]
> Go will be supported soon but for now you can build it from the source.

If you have any questions or need help with Cost Monitoring Construct, you can reach out to our support team at [support@datachef.co](mailto:support@datachef.co).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_budgets as _aws_cdk_aws_budgets_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


class Budget(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cost-monitoring-construct.Budget",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "IBudgetProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365abf60160d9d6cc8dee89c5f21b008b21fbb70b2af4730efb2e44449df0d0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="clone")
    def clone(self, id: builtins.str, props: "IOptionalBudgetProps") -> "Budget":
        '''create a copy of the object with the provided changes.

        :param id: - a unique CDK Construct identifier.
        :param props: - you can choose to optionally pass all the initializer parameters of this class as the changes you wish to have on the cloned object.

        :return: - copy of the object
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a350614df87c53ab8caa4fc361d8d650ea5e9beb6877f33eef51ea4acb253a49)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast("Budget", jsii.invoke(self, "clone", [id, props]))


@jsii.enum(jsii_type="cost-monitoring-construct.ComparisonOperator")
class ComparisonOperator(enum.Enum):
    EQUAL_TO = "EQUAL_TO"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"


@jsii.interface(jsii_type="cost-monitoring-construct.IBudgetAlertCondition")
class IBudgetAlertCondition(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> "TimeUnit":
        ...

    @period.setter
    def period(self, value: "TimeUnit") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        ...

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        ...

    @comparison_operator.setter
    def comparison_operator(self, value: typing.Optional[ComparisonOperator]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> typing.Optional["NotificationType"]:
        ...

    @notification_type.setter
    def notification_type(self, value: typing.Optional["NotificationType"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="thresholdType")
    def threshold_type(self) -> typing.Optional["ThresholdType"]:
        ...

    @threshold_type.setter
    def threshold_type(self, value: typing.Optional["ThresholdType"]) -> None:
        ...


class _IBudgetAlertConditionProxy:
    __jsii_type__: typing.ClassVar[str] = "cost-monitoring-construct.IBudgetAlertCondition"

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> "TimeUnit":
        return typing.cast("TimeUnit", jsii.get(self, "period"))

    @period.setter
    def period(self, value: "TimeUnit") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a169997964e68f9d19c92ce3681e8f9efeec736b981c0befeeb7bf540186d6c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d9b3eaec9f4485a3ddded23be6aed3343095b2464caebaf02c21b5c22ffe09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value)

    @builtins.property
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        return typing.cast(typing.Optional[ComparisonOperator], jsii.get(self, "comparisonOperator"))

    @comparison_operator.setter
    def comparison_operator(self, value: typing.Optional[ComparisonOperator]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941765be17ea51d83cc81c7cc4d31757b68ccb902e55f48001b16eb99bc02d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparisonOperator", value)

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> typing.Optional["NotificationType"]:
        return typing.cast(typing.Optional["NotificationType"], jsii.get(self, "notificationType"))

    @notification_type.setter
    def notification_type(self, value: typing.Optional["NotificationType"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d3275731d903f185b22e4969b84d7be15eb031568fd289b3a7cfbf14085b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationType", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdType")
    def threshold_type(self) -> typing.Optional["ThresholdType"]:
        return typing.cast(typing.Optional["ThresholdType"], jsii.get(self, "thresholdType"))

    @threshold_type.setter
    def threshold_type(self, value: typing.Optional["ThresholdType"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141842f8df9b1f3b393cce1658422c98a7c96cd198df6b1077a7c3a376cbc4ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBudgetAlertCondition).__jsii_proxy_class__ = lambda : _IBudgetAlertConditionProxy


@jsii.interface(jsii_type="cost-monitoring-construct.IBudgetProps")
class IBudgetProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="alertContdition")
    def alert_contdition(self) -> IBudgetAlertCondition:
        ...

    @alert_contdition.setter
    def alert_contdition(self, value: IBudgetAlertCondition) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        ...

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(
        self,
    ) -> typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]:
        ...

    @subscribers.setter
    def subscribers(
        self,
        value: typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["ITag"]]:
        ...

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["ITag"]]) -> None:
        ...


class _IBudgetPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cost-monitoring-construct.IBudgetProps"

    @builtins.property
    @jsii.member(jsii_name="alertContdition")
    def alert_contdition(self) -> IBudgetAlertCondition:
        return typing.cast(IBudgetAlertCondition, jsii.get(self, "alertContdition"))

    @alert_contdition.setter
    def alert_contdition(self, value: IBudgetAlertCondition) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5954d10e61d98c2cbf7c511ee8cc8c128ff6b334be4917f3c01bba48b30d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertContdition", value)

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c6267b12fffa4db4d8c7a0ee1bf34af8b968a7d4c1d329bfe8dd929668b6a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value)

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(
        self,
    ) -> typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]:
        return typing.cast(typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty], jsii.get(self, "subscribers"))

    @subscribers.setter
    def subscribers(
        self,
        value: typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad4c99034db5050b56b20cea9bc27b21e6bd8aa0b3bbaabcea9472d066f6726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribers", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["ITag"]]:
        return typing.cast(typing.Optional[typing.List["ITag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["ITag"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01cadb5ce89443411d9f8be81bc489f97a384a21bb987974a840091bcda8024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBudgetProps).__jsii_proxy_class__ = lambda : _IBudgetPropsProxy


class IBudgetStrategy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cost-monitoring-construct.IBudgetStrategy",
):
    def __init__(
        self,
        construct: _aws_cdk_ceddda9d.Stack,
        props: "IBudgetStrategyProps",
    ) -> None:
        '''defines the stratcure of a BudgetStategy class.

        :param construct: - use to define it's resources inside it.
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c103112253cd3c3b4a508bceef01e19a4654841dc64975248745d9e0ced2402b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [construct, props])

    @jsii.member(jsii_name="createBudgets")
    def create_budgets(self) -> None:
        '''creates all the daily, monthly, quaryerly, and yearly budgets based on the implementation of the related methods.'''
        return typing.cast(None, jsii.invoke(self, "createBudgets", []))

    @jsii.member(jsii_name="createDailyBudgets")
    @abc.abstractmethod
    def _create_daily_budgets(
        self,
        daily_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param daily_limit: -
        :param subscribers: -
        '''
        ...

    @jsii.member(jsii_name="createMonthlyBudgets")
    @abc.abstractmethod
    def _create_monthly_budgets(
        self,
        monthly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param monthly_limit: -
        :param subscribers: -
        '''
        ...

    @jsii.member(jsii_name="createQuarterlyBudgets")
    @abc.abstractmethod
    def _create_quarterly_budgets(
        self,
        quarterly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param quarterly_limit: -
        :param subscribers: -
        '''
        ...

    @jsii.member(jsii_name="createYearlyBudgets")
    @abc.abstractmethod
    def _create_yearly_budgets(
        self,
        yearly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param yearly_limit: -
        :param subscribers: -
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dailyLimit")
    def daily_limit(self) -> jsii.Number:
        '''calculates daily limit based on the provided monthly limit.'''
        return typing.cast(jsii.Number, jsii.get(self, "dailyLimit"))

    @builtins.property
    @jsii.member(jsii_name="monthlyLimit")
    def monthly_limit(self) -> jsii.Number:
        '''returns montly limit.'''
        return typing.cast(jsii.Number, jsii.get(self, "monthlyLimit"))

    @builtins.property
    @jsii.member(jsii_name="quarterlyLimit")
    def quarterly_limit(self) -> jsii.Number:
        '''calculates quarterly limit based on the provided monthly limit.'''
        return typing.cast(jsii.Number, jsii.get(self, "quarterlyLimit"))

    @builtins.property
    @jsii.member(jsii_name="yearlyLimit")
    def yearly_limit(self) -> jsii.Number:
        '''calculates yearly limit based on the provided daily budget.'''
        return typing.cast(jsii.Number, jsii.get(self, "yearlyLimit"))

    @builtins.property
    @jsii.member(jsii_name="defaultTopic")
    def default_topic(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.Topic]:
        '''Return default SNS topic only if the defultTopic prop has been passed when instantiating.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.Topic], jsii.get(self, "defaultTopic"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def _stack(self) -> _aws_cdk_ceddda9d.Stack:
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @_stack.setter
    def _stack(self, value: _aws_cdk_ceddda9d.Stack) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c09ac1909e4689d840a7c9759a8f8671b78d2e8cf9832d77ab37ead4c46794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stack", value)


class _IBudgetStrategyProxy(IBudgetStrategy):
    @jsii.member(jsii_name="createDailyBudgets")
    def _create_daily_budgets(
        self,
        daily_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param daily_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2418963c86953abe3fe1c52596665e0c9e458979f69b0c5ed3f1a241de12046b)
            check_type(argname="argument daily_limit", value=daily_limit, expected_type=type_hints["daily_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createDailyBudgets", [daily_limit, subscribers]))

    @jsii.member(jsii_name="createMonthlyBudgets")
    def _create_monthly_budgets(
        self,
        monthly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param monthly_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c206dcbed3af644b761add25dafe652d210f5bbd09316dfbaab214a999e511)
            check_type(argname="argument monthly_limit", value=monthly_limit, expected_type=type_hints["monthly_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createMonthlyBudgets", [monthly_limit, subscribers]))

    @jsii.member(jsii_name="createQuarterlyBudgets")
    def _create_quarterly_budgets(
        self,
        quarterly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param quarterly_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d109b6c2bb0ffe1d9fd3a539d15e3522c0ed624e109f9bdb891f602b24cf7366)
            check_type(argname="argument quarterly_limit", value=quarterly_limit, expected_type=type_hints["quarterly_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createQuarterlyBudgets", [quarterly_limit, subscribers]))

    @jsii.member(jsii_name="createYearlyBudgets")
    def _create_yearly_budgets(
        self,
        yearly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param yearly_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f971b015d291697453170a75af2992e8d4e7bb3b3a1de0d937afbe6bcdefcb1)
            check_type(argname="argument yearly_limit", value=yearly_limit, expected_type=type_hints["yearly_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createYearlyBudgets", [yearly_limit, subscribers]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, IBudgetStrategy).__jsii_proxy_class__ = lambda : _IBudgetStrategyProxy


@jsii.interface(jsii_type="cost-monitoring-construct.IBudgetStrategyProps")
class IBudgetStrategyProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="monthlyLimitInDollars")
    def monthly_limit_in_dollars(self) -> jsii.Number:
        ...

    @monthly_limit_in_dollars.setter
    def monthly_limit_in_dollars(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultTopic")
    def default_topic(self) -> typing.Optional[builtins.str]:
        ...

    @default_topic.setter
    def default_topic(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(self) -> typing.Optional[typing.List[builtins.str]]:
        ...

    @subscribers.setter
    def subscribers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...


class _IBudgetStrategyPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cost-monitoring-construct.IBudgetStrategyProps"

    @builtins.property
    @jsii.member(jsii_name="monthlyLimitInDollars")
    def monthly_limit_in_dollars(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthlyLimitInDollars"))

    @monthly_limit_in_dollars.setter
    def monthly_limit_in_dollars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c41c81462322c9b6739b44cf119d812e914ce08ff18786aff1ba9fc132d07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthlyLimitInDollars", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTopic")
    def default_topic(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTopic"))

    @default_topic.setter
    def default_topic(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2072df5054cedd9785787c9e96d3ad7f9897375df6988c2471bddba94a014f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTopic", value)

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subscribers"))

    @subscribers.setter
    def subscribers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7097f679e2b7535ab4395d449452bc902f33d9088d3294c3a999153b5df55fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribers", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBudgetStrategyProps).__jsii_proxy_class__ = lambda : _IBudgetStrategyPropsProxy


@jsii.interface(jsii_type="cost-monitoring-construct.IOptionalBudgetAlertCondition")
class IOptionalBudgetAlertCondition(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        ...

    @comparison_operator.setter
    def comparison_operator(self, value: typing.Optional[ComparisonOperator]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> typing.Optional["NotificationType"]:
        ...

    @notification_type.setter
    def notification_type(self, value: typing.Optional["NotificationType"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional["TimeUnit"]:
        ...

    @period.setter
    def period(self, value: typing.Optional["TimeUnit"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> typing.Optional[jsii.Number]:
        ...

    @threshold.setter
    def threshold(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="thresholdType")
    def threshold_type(self) -> typing.Optional["ThresholdType"]:
        ...

    @threshold_type.setter
    def threshold_type(self, value: typing.Optional["ThresholdType"]) -> None:
        ...


class _IOptionalBudgetAlertConditionProxy:
    __jsii_type__: typing.ClassVar[str] = "cost-monitoring-construct.IOptionalBudgetAlertCondition"

    @builtins.property
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        return typing.cast(typing.Optional[ComparisonOperator], jsii.get(self, "comparisonOperator"))

    @comparison_operator.setter
    def comparison_operator(self, value: typing.Optional[ComparisonOperator]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d072ebf62d46641c750811e356317d82231f397276302d0a3eb26b8ece143a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparisonOperator", value)

    @builtins.property
    @jsii.member(jsii_name="notificationType")
    def notification_type(self) -> typing.Optional["NotificationType"]:
        return typing.cast(typing.Optional["NotificationType"], jsii.get(self, "notificationType"))

    @notification_type.setter
    def notification_type(self, value: typing.Optional["NotificationType"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a746b33d82eacc73931fad682bf3ca3ce087b205d28871fd39544c47ba3defa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationType", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional["TimeUnit"]:
        return typing.cast(typing.Optional["TimeUnit"], jsii.get(self, "period"))

    @period.setter
    def period(self, value: typing.Optional["TimeUnit"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0cc1df44fbae5569a0a8b80838b2ebc47f9abc3efc95052b796d7067b9d350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225913eb73d9be55a606d4b7b19b163c0330ef5f9b7af4df4a2925e8d0ee979d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdType")
    def threshold_type(self) -> typing.Optional["ThresholdType"]:
        return typing.cast(typing.Optional["ThresholdType"], jsii.get(self, "thresholdType"))

    @threshold_type.setter
    def threshold_type(self, value: typing.Optional["ThresholdType"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306cfb918c9d017f5f14d8521e69ae63296af04aeb1ca17cccbd974a5f1825c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOptionalBudgetAlertCondition).__jsii_proxy_class__ = lambda : _IOptionalBudgetAlertConditionProxy


@jsii.interface(jsii_type="cost-monitoring-construct.IOptionalBudgetProps")
class IOptionalBudgetProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="alertContdition")
    def alert_contdition(self) -> typing.Optional[IOptionalBudgetAlertCondition]:
        ...

    @alert_contdition.setter
    def alert_contdition(
        self,
        value: typing.Optional[IOptionalBudgetAlertCondition],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> typing.Optional[jsii.Number]:
        ...

    @limit.setter
    def limit(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]]:
        ...

    @subscribers.setter
    def subscribers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["ITag"]]:
        ...

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["ITag"]]) -> None:
        ...


class _IOptionalBudgetPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cost-monitoring-construct.IOptionalBudgetProps"

    @builtins.property
    @jsii.member(jsii_name="alertContdition")
    def alert_contdition(self) -> typing.Optional[IOptionalBudgetAlertCondition]:
        return typing.cast(typing.Optional[IOptionalBudgetAlertCondition], jsii.get(self, "alertContdition"))

    @alert_contdition.setter
    def alert_contdition(
        self,
        value: typing.Optional[IOptionalBudgetAlertCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904e8dbfdaf6f1a9274b18cc260fa0a10ccc120aedfd9dba2fa4fc05b7d9012d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertContdition", value)

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b40178e1a8af563fbc00bd8173dcb93b691eca1abf1da9ab1dc80d0f44ab900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value)

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]], jsii.get(self, "subscribers"))

    @subscribers.setter
    def subscribers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e88062b5086f28ca03e4603ff466e7c2e475f1094460cb3aad2fddd55a77ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribers", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["ITag"]]:
        return typing.cast(typing.Optional[typing.List["ITag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["ITag"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301d2e7d16fe70795a0fd80f64a53a5473d56f3ade9ab3f20bbc1eb5969ac9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOptionalBudgetProps).__jsii_proxy_class__ = lambda : _IOptionalBudgetPropsProxy


@jsii.interface(jsii_type="cost-monitoring-construct.ITag")
class ITag(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        ...

    @key.setter
    def key(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Union[builtins.str, jsii.Number]:
        ...

    @value.setter
    def value(self, value: typing.Union[builtins.str, jsii.Number]) -> None:
        ...


class _ITagProxy:
    __jsii_type__: typing.ClassVar[str] = "cost-monitoring-construct.ITag"

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3209cba49746d7aa7fa769c58b08e731e699068a2d32c395826c241eaffeba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Union[builtins.str, jsii.Number]:
        return typing.cast(typing.Union[builtins.str, jsii.Number], jsii.get(self, "value"))

    @value.setter
    def value(self, value: typing.Union[builtins.str, jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245f2dade1ea170c8f3e896f6d1d8f0ef4cbf829a94e0f9e71ae73a78f070791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITag).__jsii_proxy_class__ = lambda : _ITagProxy


@jsii.enum(jsii_type="cost-monitoring-construct.NotificationType")
class NotificationType(enum.Enum):
    ACTUAL = "ACTUAL"
    FORECASTED = "FORECASTED"


@jsii.enum(jsii_type="cost-monitoring-construct.SubscriptionType")
class SubscriptionType(enum.Enum):
    EMAIL = "EMAIL"
    SNS = "SNS"


@jsii.enum(jsii_type="cost-monitoring-construct.ThresholdType")
class ThresholdType(enum.Enum):
    ABSOLUTE_VALUE = "ABSOLUTE_VALUE"
    PERCENTAGE = "PERCENTAGE"


@jsii.enum(jsii_type="cost-monitoring-construct.TimeUnit")
class TimeUnit(enum.Enum):
    DAILY = "DAILY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"


class AccountCostMonitoring(
    IBudgetStrategy,
    metaclass=jsii.JSIIMeta,
    jsii_type="cost-monitoring-construct.AccountCostMonitoring",
):
    def __init__(
        self,
        construct: _aws_cdk_ceddda9d.Stack,
        props: IBudgetStrategyProps,
    ) -> None:
        '''defines the stratcure of a BudgetStategy class.

        :param construct: - use to define it's resources inside it.
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab80f52956a180c4e31c638aa5044e3d883d8ca22a480ae4bf4b446ebb236fe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [construct, props])

    @jsii.member(jsii_name="createDailyBudgets")
    def _create_daily_budgets(
        self,
        daily_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param daily_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79bd14befd09f8ce4c9791dc5321f0ba8ef3dfeeeeab036561851a48800bb039)
            check_type(argname="argument daily_limit", value=daily_limit, expected_type=type_hints["daily_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createDailyBudgets", [daily_limit, subscribers]))

    @jsii.member(jsii_name="createMonthlyBudgets")
    def _create_monthly_budgets(
        self,
        monthly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param monthly_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e3eb9399579740eda7f8c11749e6712953ff9f0c9560d581332c37ce4b3b78)
            check_type(argname="argument monthly_limit", value=monthly_limit, expected_type=type_hints["monthly_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createMonthlyBudgets", [monthly_limit, subscribers]))

    @jsii.member(jsii_name="createQuarterlyBudgets")
    def _create_quarterly_budgets(
        self,
        _quarterly_limit: jsii.Number,
        _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param _quarterly_limit: -
        :param _subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c03f91501d66b1deef9ebc5fbb1c5dbcff200ba60247f40a60ea39cab73476)
            check_type(argname="argument _quarterly_limit", value=_quarterly_limit, expected_type=type_hints["_quarterly_limit"])
            check_type(argname="argument _subscribers", value=_subscribers, expected_type=type_hints["_subscribers"])
        return typing.cast(None, jsii.invoke(self, "createQuarterlyBudgets", [_quarterly_limit, _subscribers]))

    @jsii.member(jsii_name="createYearlyBudgets")
    def _create_yearly_budgets(
        self,
        _yearly_limit: jsii.Number,
        _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param _yearly_limit: -
        :param _subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b3e95ae6c422315ac1541d4002a655239992563aa66ebdd1a2ce0a3d36bcec)
            check_type(argname="argument _yearly_limit", value=_yearly_limit, expected_type=type_hints["_yearly_limit"])
            check_type(argname="argument _subscribers", value=_subscribers, expected_type=type_hints["_subscribers"])
        return typing.cast(None, jsii.invoke(self, "createYearlyBudgets", [_yearly_limit, _subscribers]))


class ApplicationCostMonitoring(
    IBudgetStrategy,
    metaclass=jsii.JSIIMeta,
    jsii_type="cost-monitoring-construct.ApplicationCostMonitoring",
):
    def __init__(
        self,
        stack: _aws_cdk_ceddda9d.Stack,
        props: "ApplicationCostMonitoringProps",
    ) -> None:
        '''Default Application CostMonitoring class that implements daily and monthly budgets.

        :param stack: - default stack to track its resources and it will be used to define Budget resources in it.
        :param props: -

        Example::

            .com']
            });
            
            budgetStratgy.monitor();
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361ff8775d5ca30a358315f98c5b27b9eb15f57051ae67ebfad4c5e0c037aedf)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [stack, props])

    @jsii.member(jsii_name="createDailyBudgets")
    def _create_daily_budgets(
        self,
        daily_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param daily_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a43e31b85a1187100c257ebb94b68ea4041c3f8a9670ca7f5d4e6d18a1d910)
            check_type(argname="argument daily_limit", value=daily_limit, expected_type=type_hints["daily_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createDailyBudgets", [daily_limit, subscribers]))

    @jsii.member(jsii_name="createMonthlyBudgets")
    def _create_monthly_budgets(
        self,
        monthly_limit: jsii.Number,
        subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param monthly_limit: -
        :param subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc959ece21ecd0ad297312353ed636de5dfd8273593b84e32db13255f5bb8e7)
            check_type(argname="argument monthly_limit", value=monthly_limit, expected_type=type_hints["monthly_limit"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        return typing.cast(None, jsii.invoke(self, "createMonthlyBudgets", [monthly_limit, subscribers]))

    @jsii.member(jsii_name="createQuarterlyBudgets")
    def _create_quarterly_budgets(
        self,
        _quarterly_limit: jsii.Number,
        _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param _quarterly_limit: -
        :param _subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad2f26894578dee8d948aaf2ef3ff86527bc1a72a041c336716d6aa6111d1ff)
            check_type(argname="argument _quarterly_limit", value=_quarterly_limit, expected_type=type_hints["_quarterly_limit"])
            check_type(argname="argument _subscribers", value=_subscribers, expected_type=type_hints["_subscribers"])
        return typing.cast(None, jsii.invoke(self, "createQuarterlyBudgets", [_quarterly_limit, _subscribers]))

    @jsii.member(jsii_name="createYearlyBudgets")
    def _create_yearly_budgets(
        self,
        _yearly_limit: jsii.Number,
        _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param _yearly_limit: -
        :param _subscribers: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe3f11eca3ecc235e4a44d856cb8c6714452a9c090cd9d7441c419f3771b6c0)
            check_type(argname="argument _yearly_limit", value=_yearly_limit, expected_type=type_hints["_yearly_limit"])
            check_type(argname="argument _subscribers", value=_subscribers, expected_type=type_hints["_subscribers"])
        return typing.cast(None, jsii.invoke(self, "createYearlyBudgets", [_yearly_limit, _subscribers]))

    @jsii.member(jsii_name="monitor")
    def monitor(self) -> None:
        '''Creates all the alarms, budgets and tags all resources with the application's name.'''
        return typing.cast(None, jsii.invoke(self, "monitor", []))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @builtins.property
    @jsii.member(jsii_name="applicationTagKey")
    def _application_tag_key(self) -> builtins.str:
        '''Default key name for application tag.'''
        return typing.cast(builtins.str, jsii.get(self, "applicationTagKey"))


@jsii.interface(jsii_type="cost-monitoring-construct.IApplicationCostMonitoringProps")
class IApplicationCostMonitoringProps(IBudgetStrategyProps, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        ...

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="costAllocationTag")
    def cost_allocation_tag(self) -> typing.Optional[builtins.str]:
        ...

    @cost_allocation_tag.setter
    def cost_allocation_tag(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="otherStacksIncludedInBudget")
    def other_stacks_included_in_budget(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]]:
        ...

    @other_stacks_included_in_budget.setter
    def other_stacks_included_in_budget(
        self,
        value: typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]],
    ) -> None:
        ...


class _IApplicationCostMonitoringPropsProxy(
    jsii.proxy_for(IBudgetStrategyProps), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "cost-monitoring-construct.IApplicationCostMonitoringProps"

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0908894562bb6b1e002cfc2998d89bf3aa6fd8824c3de1bb8bec8ef25bb81a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="costAllocationTag")
    def cost_allocation_tag(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "costAllocationTag"))

    @cost_allocation_tag.setter
    def cost_allocation_tag(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0672d13ac4327bb5a1ad546e7a493f18b1ad64186dde6abe7e36ad71223a3f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "costAllocationTag", value)

    @builtins.property
    @jsii.member(jsii_name="otherStacksIncludedInBudget")
    def other_stacks_included_in_budget(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]], jsii.get(self, "otherStacksIncludedInBudget"))

    @other_stacks_included_in_budget.setter
    def other_stacks_included_in_budget(
        self,
        value: typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6cbb5b07678e3fafe88dc1a98554194ef0f287b295a5a466ce4f76da7ea988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "otherStacksIncludedInBudget", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplicationCostMonitoringProps).__jsii_proxy_class__ = lambda : _IApplicationCostMonitoringPropsProxy


@jsii.implements(IApplicationCostMonitoringProps)
class ApplicationCostMonitoringProps(
    metaclass=jsii.JSIIMeta,
    jsii_type="cost-monitoring-construct.ApplicationCostMonitoringProps",
):
    def __init__(
        self,
        application_name: builtins.str,
        monthly_limit_in_dollars: jsii.Number,
        other_stacks_included_in_budget: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Stack]] = None,
        default_topic: typing.Optional[builtins.str] = None,
        subscribers: typing.Optional[typing.Sequence[builtins.str]] = None,
        cost_allocation_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param application_name: - the name of application to label resources with it.
        :param monthly_limit_in_dollars: - montly limit in US Dollors.
        :param other_stacks_included_in_budget: - optional other stack to track their resources alog with the default stack.
        :param default_topic: - default SNS topic name. Only if provided, the BudgetStratgy creates an SNS topic and send notifications to it.
        :param subscribers: - list of email address that the CostMonitoring will use to send alerts to.
        :param cost_allocation_tag: - Tag key used to track resources' expenditure. Only if provided, it will be used to tag the application resources. Defaults to ``cm:application``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016611925949da4facbba95bcddcf14217d235eea769e2db3a3d240c6ca86d73)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument monthly_limit_in_dollars", value=monthly_limit_in_dollars, expected_type=type_hints["monthly_limit_in_dollars"])
            check_type(argname="argument other_stacks_included_in_budget", value=other_stacks_included_in_budget, expected_type=type_hints["other_stacks_included_in_budget"])
            check_type(argname="argument default_topic", value=default_topic, expected_type=type_hints["default_topic"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
            check_type(argname="argument cost_allocation_tag", value=cost_allocation_tag, expected_type=type_hints["cost_allocation_tag"])
        jsii.create(self.__class__, self, [application_name, monthly_limit_in_dollars, other_stacks_included_in_budget, default_topic, subscribers, cost_allocation_tag])

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''- the name of application to label resources with it.'''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd4ce542700b2deac40811890f4429d90eac081bd29d08415e6ce8667697422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="monthlyLimitInDollars")
    def monthly_limit_in_dollars(self) -> jsii.Number:
        '''- montly limit in US Dollors.'''
        return typing.cast(jsii.Number, jsii.get(self, "monthlyLimitInDollars"))

    @monthly_limit_in_dollars.setter
    def monthly_limit_in_dollars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b7dbe15daa64f31317dedf1362713156a13c2d526b10bae05bb824fb1852b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthlyLimitInDollars", value)

    @builtins.property
    @jsii.member(jsii_name="costAllocationTag")
    def cost_allocation_tag(self) -> typing.Optional[builtins.str]:
        '''- Tag key used to track resources' expenditure.

        Only if provided, it will be used to tag the application resources. Defaults to ``cm:application``
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "costAllocationTag"))

    @cost_allocation_tag.setter
    def cost_allocation_tag(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd683e50b33baeaf6f59fc99784ce52773a612c0f5a480e422ab4972f7f6e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "costAllocationTag", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTopic")
    def default_topic(self) -> typing.Optional[builtins.str]:
        '''- default SNS topic name.

        Only if provided, the BudgetStratgy creates an SNS topic and send notifications to it.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTopic"))

    @default_topic.setter
    def default_topic(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36b5adee3e84bbffda1fbfb9801304b1780cd8ef3dc089586a0aeee043a09a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTopic", value)

    @builtins.property
    @jsii.member(jsii_name="otherStacksIncludedInBudget")
    def other_stacks_included_in_budget(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]]:
        '''- optional other stack to track their resources alog with the default stack.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]], jsii.get(self, "otherStacksIncludedInBudget"))

    @other_stacks_included_in_budget.setter
    def other_stacks_included_in_budget(
        self,
        value: typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ca7aaaa6cac405f55855e5078ed65603a6f03c771242fe182f13cf406a81a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "otherStacksIncludedInBudget", value)

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''- list of email address that the CostMonitoring will use to send alerts to.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subscribers"))

    @subscribers.setter
    def subscribers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac5a7c82099fee82a0b4f1e50169bd023e5de76ee7c699ab88840159ea951e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribers", value)


__all__ = [
    "AccountCostMonitoring",
    "ApplicationCostMonitoring",
    "ApplicationCostMonitoringProps",
    "Budget",
    "ComparisonOperator",
    "IApplicationCostMonitoringProps",
    "IBudgetAlertCondition",
    "IBudgetProps",
    "IBudgetStrategy",
    "IBudgetStrategyProps",
    "IOptionalBudgetAlertCondition",
    "IOptionalBudgetProps",
    "ITag",
    "NotificationType",
    "SubscriptionType",
    "ThresholdType",
    "TimeUnit",
]

publication.publish()

def _typecheckingstub__365abf60160d9d6cc8dee89c5f21b008b21fbb70b2af4730efb2e44449df0d0a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IBudgetProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a350614df87c53ab8caa4fc361d8d650ea5e9beb6877f33eef51ea4acb253a49(
    id: builtins.str,
    props: IOptionalBudgetProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a169997964e68f9d19c92ce3681e8f9efeec736b981c0befeeb7bf540186d6c6(
    value: TimeUnit,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d9b3eaec9f4485a3ddded23be6aed3343095b2464caebaf02c21b5c22ffe09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941765be17ea51d83cc81c7cc4d31757b68ccb902e55f48001b16eb99bc02d90(
    value: typing.Optional[ComparisonOperator],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d3275731d903f185b22e4969b84d7be15eb031568fd289b3a7cfbf14085b6b(
    value: typing.Optional[NotificationType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141842f8df9b1f3b393cce1658422c98a7c96cd198df6b1077a7c3a376cbc4ee(
    value: typing.Optional[ThresholdType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5954d10e61d98c2cbf7c511ee8cc8c128ff6b334be4917f3c01bba48b30d8b(
    value: IBudgetAlertCondition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c6267b12fffa4db4d8c7a0ee1bf34af8b968a7d4c1d329bfe8dd929668b6a0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad4c99034db5050b56b20cea9bc27b21e6bd8aa0b3bbaabcea9472d066f6726(
    value: typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01cadb5ce89443411d9f8be81bc489f97a384a21bb987974a840091bcda8024(
    value: typing.Optional[typing.List[ITag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c103112253cd3c3b4a508bceef01e19a4654841dc64975248745d9e0ced2402b(
    construct: _aws_cdk_ceddda9d.Stack,
    props: IBudgetStrategyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c09ac1909e4689d840a7c9759a8f8671b78d2e8cf9832d77ab37ead4c46794(
    value: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2418963c86953abe3fe1c52596665e0c9e458979f69b0c5ed3f1a241de12046b(
    daily_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c206dcbed3af644b761add25dafe652d210f5bbd09316dfbaab214a999e511(
    monthly_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d109b6c2bb0ffe1d9fd3a539d15e3522c0ed624e109f9bdb891f602b24cf7366(
    quarterly_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f971b015d291697453170a75af2992e8d4e7bb3b3a1de0d937afbe6bcdefcb1(
    yearly_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c41c81462322c9b6739b44cf119d812e914ce08ff18786aff1ba9fc132d07d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2072df5054cedd9785787c9e96d3ad7f9897375df6988c2471bddba94a014f6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7097f679e2b7535ab4395d449452bc902f33d9088d3294c3a999153b5df55fc8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d072ebf62d46641c750811e356317d82231f397276302d0a3eb26b8ece143a(
    value: typing.Optional[ComparisonOperator],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a746b33d82eacc73931fad682bf3ca3ce087b205d28871fd39544c47ba3defa(
    value: typing.Optional[NotificationType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0cc1df44fbae5569a0a8b80838b2ebc47f9abc3efc95052b796d7067b9d350(
    value: typing.Optional[TimeUnit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225913eb73d9be55a606d4b7b19b163c0330ef5f9b7af4df4a2925e8d0ee979d(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306cfb918c9d017f5f14d8521e69ae63296af04aeb1ca17cccbd974a5f1825c9(
    value: typing.Optional[ThresholdType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904e8dbfdaf6f1a9274b18cc260fa0a10ccc120aedfd9dba2fa4fc05b7d9012d(
    value: typing.Optional[IOptionalBudgetAlertCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b40178e1a8af563fbc00bd8173dcb93b691eca1abf1da9ab1dc80d0f44ab900(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e88062b5086f28ca03e4603ff466e7c2e475f1094460cb3aad2fddd55a77ed0(
    value: typing.Optional[typing.List[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301d2e7d16fe70795a0fd80f64a53a5473d56f3ade9ab3f20bbc1eb5969ac9d6(
    value: typing.Optional[typing.List[ITag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3209cba49746d7aa7fa769c58b08e731e699068a2d32c395826c241eaffeba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245f2dade1ea170c8f3e896f6d1d8f0ef4cbf829a94e0f9e71ae73a78f070791(
    value: typing.Union[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab80f52956a180c4e31c638aa5044e3d883d8ca22a480ae4bf4b446ebb236fe(
    construct: _aws_cdk_ceddda9d.Stack,
    props: IBudgetStrategyProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bd14befd09f8ce4c9791dc5321f0ba8ef3dfeeeeab036561851a48800bb039(
    daily_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e3eb9399579740eda7f8c11749e6712953ff9f0c9560d581332c37ce4b3b78(
    monthly_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c03f91501d66b1deef9ebc5fbb1c5dbcff200ba60247f40a60ea39cab73476(
    _quarterly_limit: jsii.Number,
    _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b3e95ae6c422315ac1541d4002a655239992563aa66ebdd1a2ce0a3d36bcec(
    _yearly_limit: jsii.Number,
    _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361ff8775d5ca30a358315f98c5b27b9eb15f57051ae67ebfad4c5e0c037aedf(
    stack: _aws_cdk_ceddda9d.Stack,
    props: ApplicationCostMonitoringProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a43e31b85a1187100c257ebb94b68ea4041c3f8a9670ca7f5d4e6d18a1d910(
    daily_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc959ece21ecd0ad297312353ed636de5dfd8273593b84e32db13255f5bb8e7(
    monthly_limit: jsii.Number,
    subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad2f26894578dee8d948aaf2ef3ff86527bc1a72a041c336716d6aa6111d1ff(
    _quarterly_limit: jsii.Number,
    _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe3f11eca3ecc235e4a44d856cb8c6714452a9c090cd9d7441c419f3771b6c0(
    _yearly_limit: jsii.Number,
    _subscribers: typing.Sequence[typing.Union[_aws_cdk_aws_budgets_ceddda9d.CfnBudget.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0908894562bb6b1e002cfc2998d89bf3aa6fd8824c3de1bb8bec8ef25bb81a73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0672d13ac4327bb5a1ad546e7a493f18b1ad64186dde6abe7e36ad71223a3f67(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6cbb5b07678e3fafe88dc1a98554194ef0f287b295a5a466ce4f76da7ea988(
    value: typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016611925949da4facbba95bcddcf14217d235eea769e2db3a3d240c6ca86d73(
    application_name: builtins.str,
    monthly_limit_in_dollars: jsii.Number,
    other_stacks_included_in_budget: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.Stack]] = None,
    default_topic: typing.Optional[builtins.str] = None,
    subscribers: typing.Optional[typing.Sequence[builtins.str]] = None,
    cost_allocation_tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd4ce542700b2deac40811890f4429d90eac081bd29d08415e6ce8667697422(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b7dbe15daa64f31317dedf1362713156a13c2d526b10bae05bb824fb1852b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd683e50b33baeaf6f59fc99784ce52773a612c0f5a480e422ab4972f7f6e2b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36b5adee3e84bbffda1fbfb9801304b1780cd8ef3dc089586a0aeee043a09a7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ca7aaaa6cac405f55855e5078ed65603a6f03c771242fe182f13cf406a81a0(
    value: typing.Optional[typing.List[_aws_cdk_ceddda9d.Stack]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac5a7c82099fee82a0b4f1e50169bd023e5de76ee7c699ab88840159ea951e2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass
